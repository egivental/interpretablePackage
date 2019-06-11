package lab0Test;

public class Main {
	
	public static double power(double x, int exp)
	{
		if(exp == 0)
			return 1;
		else
		{
			double numb = x;
			for(int i = 1; i < exp; i++)
				numb = numb * x;
			return numb;
		}
	}
	
	public static int GCD(int num1, int num2)
	{
		while( num1 != 0 && num2 != 0)
			{
				if(num1 > num2)
					num1 = num1%num2;
				else // num2 > num1
					num2 = num2%num1;
			}
		if(num1 == 0)
			return num2;
		else
			return num1;
	}
	
	public static boolean isPrime(int num)
	{
		if(num<2)
			return false;
		
		int counter = 2;
		while(counter < num)
		{
			if(num % counter == 0)
				return false;
			counter++;
		}
		
		return true;
	}
	
	public static int roundMod(double num)
	{
		if(num > 0) // input is positive
		{
			if(num%1 >= 0.5)
				return 1 + (int) num;
			else // the decimal is less than 0.5
				return (int) num;
		}
		else
		{
			if(num%1 <= -0.5)
				return -1 + (int) num;
			else
				return (int) num;
		}
	}
	
	public enum className {cs105, cs106, cs231, cs240, cs245, cs246;}
	public static void prerequisites(className major)
	{
		switch(major)
		{
		case cs105:
			System.out.println("none");
			break;
		case cs106:
			System.out.println("cs105");
			break;
		case cs231:
			System.out.println("cs105, cs106");
			break;
		case cs240:
			System.out.println("cs105, cs106, cs231");
			break;
		case cs245:
			System.out.println("cs105, cs106, cs231");
			break;
		default:
			System.out.println("Not a major requirement");
			break;
		}
	}
}
