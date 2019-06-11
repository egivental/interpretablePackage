
public class lab0 {

		public class main{
		public static void main(String[] args) {
			
			//#1 power function tests
			System.out.println(powerFor(2, 3));      // =8.0
			System.out.println(powerWhile(2, 3));    // =8.0
			
			System.out.println(powerFor(2.4, 3));    // = 13.824
			System.out.println(powerWhile(2.4, 3));  // = 13.824
			
			System.out.println(powerFor(-2.4, 3));   // = -13.824
			System.out.println(powerWhile(-2.4, 3)); // = -13.824
			
			//#2 gcd tests
			System.out.println(gcd(221, 377));       // = 13
			System.out.println(gcd(377, 221));       // = 13
			System.out.println(gcd(1836, 1998));     // = 54
			System.out.println(gcd(1998, 1836));     // = 54
			
			// #3 isPrime tests
			System.out.println(isPrimeFor(337));     // true
			System.out.println(isPrimeWhile(337));   // true
			System.out.println(isPrimeFor(2));       // true
			System.out.println(isPrimeWhile(2));     // true
			System.out.println(isPrimeFor(1));       // false
			System.out.println(isPrimeWhile(1));     // false
			System.out.println(isPrimeFor(-7));      // false
			System.out.println(isPrimeWhile(-7));    // false
			
			// #4 round tests... students most likely should do roundMod
			System.out.println(round(0));         // 0
			System.out.println(roundMod(0));      // 0
			System.out.println(roundLoop(0));     // 0
			System.out.println(round(0.0));       // 0
			System.out.println(roundMod(0.0));    // 0
			System.out.println(roundLoop(0.0));   // 0
			System.out.println(round(4.0));       // 4
			System.out.println(roundMod(4.0));    // 4
			System.out.println(roundLoop(4.0));   // 4
			System.out.println(round(-4.0));      // -4
			System.out.println(roundMod(-4.0));   // -4
			System.out.println(roundLoop(-4.0));  // -4
			System.out.println(round(5.5));       // 6
			System.out.println(roundMod(5.5));    // 6
			System.out.println(roundLoop(5.5));   // 6
			System.out.println(round(-5.5));      // -6
			System.out.println(roundMod(-5.5));   // -6
			System.out.println(roundLoop(-5.5));  // -6
			System.out.println(round(2.4));       // 2
			System.out.println(roundMod(2.4));    // 2
			System.out.println(roundLoop(2.4));   // 2
			System.out.println(round(-2.4));      // -2
			System.out.println(roundMod(-2.4));   // -2
			System.out.println(roundLoop(-2.4));  // -2
			System.out.println(round(8.7));       // 9
			System.out.println(roundMod(8.7));    // 9
			System.out.println(roundLoop(8.7));   // 9
			System.out.println(round(-8.7));      // -9
			System.out.println(roundMod(-8.7));   // -9
			System.out.println(roundLoop(-8.7));  // -9
			
			// prerequisites tests... not all courses were done and 246 was put in to test the default case.
			prerequisites(Courses.cs105);
			prerequisites(Courses.cs106);
			prerequisites(Courses.cs231);
			prerequisites(Courses.cs240);
			prerequisites(Courses.cs245);
			prerequisites(Courses.cs246);
		}
	
		//
		// #1   power function
		//
		public static double powerFor(double x, int exp)
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
		
		public static double powerWhile(double x, int exp)
		{
			if(exp == 0)
				return 1;
			else
			{
				double num=x;
				while(exp>1)
				{
					num *= x;
					exp--;
				}
				return num;
			}
		}
		
		//
		// #2, gcd
		//
		public static int gcd(int num1, int num2)
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
		
		//
		// #3, isPrime
		//
		public static boolean isPrimeFor(int num)
		{
			if(num<2)
				return false;
			
			for(int counter = 2; counter < num; counter++)
			{
				if(num % counter == 0)
					return false;
			}
			
			return true;
		}
		
		public static boolean isPrimeWhile(int num)
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
	
		
		//
		// #4, round
		//
		public static int round(double num)
		{
			if (num == 0) {return 0;}
			
			if(num>0)
			{
				if(num-(int) num >= 0.5)
					return 1 + (int) num;
				else
					return (int) num;
			}
			
			else
			{
				double absNum = round(0 - num);
				return (int) (absNum*(-1));
			}
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
		
		public static int roundLoop(double num)
		{
			if(num == 0) return 0;
			if(num>0)
			{
				double numCheck = num;
				while(numCheck-1 >= 0)
				{
					numCheck = numCheck -1;
				}
				
				if(numCheck >= 0.5)
					return 1 + (int) num;
				else
					return (int) num;
			}
			else
				return (int) (roundLoop(0-num)*-1);
		}
		
		//
		// #5, enum
		//	
		public enum Courses {cs105, cs106, cs231, cs240, cs245, cs246;}
		public static void prerequisites(Courses major)
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
	
}