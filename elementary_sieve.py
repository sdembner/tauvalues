import math 


LIST_LENGTH = 0

def read_in_periods():
    '''
    Reads in pisano periods pi(n) for n < 10000
    '''
    d = {}
    with open("pisano_periods.txt") as f:
        for line in f:
            (key, val) = line.split()
            d[int(key)] = int(val)
    return d


def calc_fib_luc(n):
    ''' Input: n (integer): calculates fib and lucas sequence 
                            upto the integer n 
        Output: fib, lucas: lists of length n where the n-th term 
                            in the list is the n-th term in the
                            corresponding sequence 
    '''
    fib = [0, 1]
    lucas = [2, 1]
    for i in range(n-2):
        fib.append(fib[i] + fib[i+1])
        lucas.append(lucas[i] + lucas[i+1])
    return fib, lucas


def modulo_info(terms, modulo):
    final = set()
    for index, value in terms: 
        final.add(index%modulo)
    return final 


def prime_sieve(n):
    # calculates all primes less than or equal to n using a sieve 
    primes = [2]
    for i in range(3, n+1):
        check = int(math.sqrt(i))
        index, composite= 0, False
        while primes[index] <= check and not composite:
            if i%primes[index] == 0: 
                composite = True
            index += 1
        if not composite:
            primes.append(i)
    return primes


def prime_factorize(n, primes):
    '''input: n (integer)
              primes (list): list of primes
       output: factorization of n as a list of tuples (factor, power)'''
    factorization = []
    for p in primes: 
        if p > math.sqrt(n):
            break
        else: 
            counter, temp = 0, n
            while temp%p == 0: 
                counter += 1
                temp = temp/p
            if counter > 0:
                factorization.append((p, counter))
    return factorization


def perfect_powers(upto, coeff1, coeff2, PoWeR):
    '''input: 
        upto (int): must be less than 10000
                    checks all primes <= upto to get information about the 
                    perfect power modulo these primes  
        coeff1 (int): for a sequence a*fib[n] + b*lucas[n], this would be a
        coeff2 (int): for a sequence a*fib[n] + b*lucas[n], this would be b
        PoWeR (int): a prime, and looks for perfect PoWeRs in the sequence 
                     a*fib[n] + b*lucas[n]

    Output: coeff1 (int), coeff 2 (int): the coefficients corresponding to the 
                                         sequence coeff1*fib[n] + coeff2*lucas[n]
            output (boolean): true if there are no perfect PoWeRs in this sequence
                              false if this is insufficient to prove there are no 
                              PoWeRs in this seqeunce 
    '''
    output = False

    fib, lucas = calc_fib_luc(upto*6)
    periods = read_in_periods()

    primesold = prime_sieve(upto*6)
    primes = []
    for p in primesold: 
        if p % PoWeR == 1 and p <= upto: 
            primes.append(p)

    dictionary = {}
    for p in primes: 
        modulo = periods[p]
        factorization = prime_factorize(modulo, primesold)

        perf_powers = set()
        for i in range(p):
            perf_powers.add((i**PoWeR)%p)

        terms_check = []
        for factor, power in factorization:
            counter = 1
            while factor**counter in dictionary and counter <= power:
                terms_check.append(factor**counter)
                counter += 1

        final = []
        for j in range(modulo):
            temp = coeff1*fib[j] + coeff2*lucas[j]
            if temp%p in perf_powers:
                sat_congruence = True
                if len(terms_check) != 0: 
                    for term in terms_check:
                        if (j % term) not in dictionary[term]: 
                            sat_congruence = False
                            break
                if sat_congruence == True: 
                    final.append((j, temp%p))
        if len(final) <= LIST_LENGTH: 
            output = True

        #update dictionary
        for factor, power in factorization:
            for count in range(1, power+1):
                temp_set = modulo_info(final, factor**count)
                if factor**count in dictionary: 
                    dictionary[factor**count] = dictionary[factor**count].intersection(temp_set)
                else: 
                    dictionary[factor**count] = temp_set
    return coeff1, coeff2, output 


if __name__ == "__main__":
    # CHANGE THESE VALUES
    power, max_upto, coeff1, coeff2 = 11, 3000, 2, 1
    print(power, perfect_powers(max_upto, coeff1, coeff2, power))
    power, max_upto, coeff1, coeff2 = 11, 3000, 1, 4
    print(power, perfect_powers(max_upto, coeff1, coeff2, power))






