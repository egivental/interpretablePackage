public class blah {

    public static void main (String[] args) {
    System.out.println("Testing power");
    System.out.println("5^4 should be 625, is: " + power(5, 4));
    System.out.println("2^10 should be 1024, is: " + power(2, 10));
    System.out.println("3^10 should be 59049,  is: " + power(3, 10));
    System.out.println("3.3^5 should be 391.35393, is: " + power(3.3, 5));
    System.out.println("2.7^4 should be 53.1441, is: " + power(2.7, 4));
    System.out.println("-5^3 should be -125,  is: " + power(-5, 3));
    System.out.println("-1^18 should be 1,  is: " + power(-1, 18));
    System.out.println("0^18 should be 0,  is: " + power(0, 18));
    System.out.println("5^0 should be 1,  is: " + power(5, 0));
    System.out.println("0^0 should be 1,  is: " + power(0, 0));

    System.out.println("Testing gcd");
    System.out.println("gcd of 40 and 8 is 8, we got " + GCD(40,8));
    System.out.println("gcd of 81 and 36 is 9, we got " + GCD(81,36));
    System.out.println("gcd of 49 and 14 is 7, we got " + GCD(49,14));
    System.out.println("gcd of 14 and 49 is 7, we got " + GCD(14,49));
    System.out.println("gcd of 5 and 128 is 1, we got " + GCD(5, 128));
    System.out.println("gcd of 10243 and 45678 is 1, we got " + GCD(10243,45678));
    System.out.println("gcd of 16384 and 32768 is 16384, we got " + GCD(16384,32768));

    System.out.println("Testing prime");
    System.out.println("9 is prime is false, we got " + isPrime(9));
    System.out.println("13 is prime is true, we got " + isPrime(13));
    System.out.println("2 is prime is true, we got " + isPrime(2));
    System.out.println("16384 is prime is false, we got " + isPrime(16384));
    System.out.println("48761 is prime is true, we got " + isPrime(48761));

    System.out.println("Testing round");
    System.out.println("4.23423 rounded is 4, we got " + round(4.23423));
    System.out.println("0.5423 rounded is 1, we got " + round(0.5423));
    System.out.println("1.21423 rounded is 1, we got " + round(1.21423));
    System.out.println("Now for some negative rounding...");
    System.out.println("-1.7623 rounded is -2, we got " + round(-1.7623));
    System.out.println("-4.2623 rounded is -4, we got " + round(-4.2623));
    System.out.println("-3.7623 rounded is -4, we got " + round(-3.7623));
    System.out.println("3.5 rounded is either 3 or 4, we got " + round(3.5));
    System.out.println("0.0001 rounded is 0, we got " + round(0.0001));

    System.out.println("Doing some prereqs now");
    for(className curr : className.values()) {
        System.out.println("Checking the prereqs for " + curr.toString());
        prerequisites(curr);
        System.out.println("-----------------------");
        }
    }
}
