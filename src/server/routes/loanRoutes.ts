import { Router, Request, Response } from 'express';
import Loan from '../../models/Loan';

const router = Router();

// Heuristic prediction function (simulates ML model behavior based on inputs)
const predictLoanApproval = (data: {
  income: number;
  creditScore: number;
  loanAmount: number;
  loanTerm: number;
  hdiIndex: number;
  age: number;
}) => {
  const { income, creditScore, loanAmount, loanTerm, hdiIndex, age } = data;

  // 1. Credit Score score (max 50 points)
  const creditPoints = ((creditScore - 300) / 550) * 50;

  // 2. Debt-to-Income ratio score (max 25 points)
  // Calculate annual payment amount
  const annualPayment = (loanAmount / loanTerm) * 12;
  const dti = annualPayment / income;
  let dtiPoints = 0;
  if (dti < 0.15) dtiPoints = 25;
  else if (dti < 0.3) dtiPoints = 15;
  else if (dti < 0.45) dtiPoints = 5;

  // 3. HDI Index score (max 15 points)
  const hdiPoints = hdiIndex * 15;

  // 4. Age score (max 10 points)
  let agePoints = 5;
  if (age >= 25 && age <= 55) agePoints = 10;
  else if (age < 21 || age > 65) agePoints = 2;

  // Total Score (out of 100)
  const totalScore = creditPoints + dtiPoints + hdiPoints + agePoints;
  let probability = Math.min(Math.max(totalScore / 100, 0.05), 0.99);

  // Forced exclusions (e.g. extremely low credit score or extreme DTI)
  if (creditScore < 450) {
    probability = Math.min(probability, 0.25);
  }
  if (dti > 0.6) {
    probability = Math.min(probability, 0.15);
  }

  // Determine status
  const status = probability >= 0.6 ? 'APPROVED' : 'REJECTED';

  // Determine risk rating
  let riskRating: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'MEDIUM';
  if (probability > 0.8) riskRating = 'LOW';
  else if (probability > 0.6) riskRating = 'MEDIUM';
  else if (probability > 0.45) riskRating = 'HIGH';
  else riskRating = 'CRITICAL';

  return { probability, status, riskRating };
};

// GET /api/loans - Get all loan applications
router.get('/', async (_req: Request, res: Response) => {
  try {
    const loans = await Loan.find().sort({ createdAt: -1 });
    res.status(200).json(loans);
  } catch (error) {
    console.error('Error fetching loans:', error);
    res.status(500).json({ message: 'Error fetching loan applications' });
  }
});

// POST /api/loans - Submit a new loan application and get prediction
router.post('/', async (req: Request, res: Response) => {
  try {
    const { borrowerName, age, income, creditScore, loanAmount, loanTerm, hdiIndex } = req.body;

    // Validation
    if (!borrowerName || !age || !income || !creditScore || !loanAmount || !loanTerm || hdiIndex === undefined) {
      res.status(400).json({ message: 'Missing required application fields' });
      return;
    }

    // Call prediction logic
    const { probability, status, riskRating } = predictLoanApproval({
      income: Number(income),
      creditScore: Number(creditScore),
      loanAmount: Number(loanAmount),
      loanTerm: Number(loanTerm),
      hdiIndex: Number(hdiIndex),
      age: Number(age)
    });

    const newLoan = new Loan({
      borrowerName,
      age: Number(age),
      income: Number(income),
      creditScore: Number(creditScore),
      loanAmount: Number(loanAmount),
      loanTerm: Number(loanTerm),
      hdiIndex: Number(hdiIndex),
      status,
      probability: parseFloat(probability.toFixed(4)),
      riskRating
    });

    await newLoan.save();
    res.status(201).json(newLoan);
  } catch (error) {
    console.error('Error creating loan application:', error);
    res.status(500).json({ message: 'Error processing loan application' });
  }
});

// GET /api/loans/stats - Get loan database statistics
router.get('/stats', async (_req: Request, res: Response) => {
  try {
    const loans = await Loan.find();
    
    const total = loans.length;
    const approved = loans.filter(l => l.status === 'APPROVED').length;
    const rejected = loans.filter(l => l.status === 'REJECTED').length;
    
    // Average metrics
    const avgIncome = total > 0 ? loans.reduce((acc, l) => acc + l.income, 0) / total : 0;
    const avgCredit = total > 0 ? loans.reduce((acc, l) => acc + l.creditScore, 0) / total : 0;
    const avgAmount = total > 0 ? loans.reduce((acc, l) => acc + l.loanAmount, 0) / total : 0;
    
    res.status(200).json({
      totalApplications: total,
      approvedCount: approved,
      rejectedCount: rejected,
      approvalRate: total > 0 ? parseFloat((approved / total).toFixed(4)) : 0,
      averageIncome: Math.round(avgIncome),
      averageCreditScore: Math.round(avgCredit),
      averageLoanAmount: Math.round(avgAmount)
    });
  } catch (error) {
    console.error('Error fetching statistics:', error);
    res.status(500).json({ message: 'Error calculating system stats' });
  }
});

export default router;
