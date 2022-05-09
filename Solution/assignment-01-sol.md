

# CMPS 2200 Assignment 1
  
$$
\\
\\
$$  
  

1. **Asymptotic notation**

  - 1a. Is $2^{n+1} \in O(2^n)$? Why or why not?

> True since $2^{n+1} = 2 * 2^n$, pick $c \ge 2$ and $n_0 = 0$



  - 1b. Is $2^{2^n} \in O(2^n)$? Why or why not?

> False. $2^{2^n} = 2^n * 2^n = 4^n$. Can't find $c$ and $n_0$ such that $4^n \le c * 2^n$ for all $n \ge n_0$  
.  
.  
.  
.  

- 1c. Is $n^{1.01} \in O(\mathrm{log}^2 n)$?

No. Any polylog grows slower than any polynomial.

so, $\log^i n \in O(n^j) ~~ \forall i,j > 0$ and visa versa: $n^j \in \Omega(\log^i n) ~~ \forall j,i > 0$

- 1d. Is $n^{1.01} \in \Omega(\mathrm{log}^2 n)$?

Yes. Any polylog grows slower than any polynomial.

so, $\log^i n \in O(n^j) ~~ \forall i,j > 0$ and visa versa: $n^j \in \Omega(\log^i n) ~~ \forall j,i > 0$

.  
.  
  - 1e. Is $\sqrt{n} \in O((\mathrm{log} n)^3)$?

No.

Observe that $\lg n = \lg \sqrt{n}^2 = 2 \lg \sqrt{n}$

So, $\sqrt{n} = 2^{(\lg n) / 2} >> \lg n$

Similarly, from our answer to 1d, $\sqrt{n} = n^{.5}$, which is a polynomial, so it grows faster than any polylog.



.  
.  
.  

   - 1f. Is $\sqrt{n} \in \Omega((\mathrm{log} n)^3)$?

Yes, from the previous question.


.    
.  
.  


2. **SPARC to Python**

Consider the following SPARC code:
$$
\begin{array}{l}
\mathit{foo}~x =   \\
~~~~\texttt{if}{}~~x \le 1~~\texttt{then}{}\\
~~~~~~~~x\\   
~~~~\texttt{else}\\
~~~~~~~~\texttt{let}{}~~(ra, rb) = (\mathit{foo}~(x-1))~~,~~(\mathit{foo}~(x-2))~~\texttt{in}{}\\  
~~~~~~~~~~~~ra + rb\\  
~~~~~~~~\texttt{end}{}.\\
\end{array}
$$ 

  - 2a. Translate this to Python code -- fill in the `def foo` method in `main.py`

```python

def foo(x):
    if x <= 1:
        return x
    else:
        return foo(x-1) + foo(x-2)
```

  - 2b. What does this function do, in your own words?

> Fibonacci sequence.




3. **Parallelism and recursion**

Consider the following function:

```python
def longest_run(myarray, key)
   """
    Input:
      `myarray`: a list of ints
      `key`: an int
    Return:
      the longest continuous sequence of `key` in `myarray`
   """
```
E.g., `longest_run([2,12,12,8,12,12,12,0,12,1], 12) == 3`
 
  - 3a. First, implement an iterative, sequential version of `longest_run` in `main.py`.


> This should just be a single for loop that keeps track of the longest run seen so far. Whenever `key` matches the next element, increment total count. If it doesn't match, reset to 0. If the total count is greater than the longest seen so far, update the longest seen so far.

```python

def longest_run(mylist, key):
    ### TODO
    seq_len = 0
    longest = 0
    for v in mylist:
        if v == key:
            seq_len += 1
        else:
            if seq_len > longest:
                longest = seq_len
            seq_len = 0
    return max(longest, seq_len)
```

  - 3b. What is the Work and Span of this implementation?

> O(n) for both. There's no parallelism.


  - 3c. Next, implement a `longest_run_recursive`, a recursive, divide and conquer implementation. This is analogous to our implementation of `sum_list_recursive`. To do so, you will need to think about how to combine partial solutions from each recursive call. Make use of the provided class `Result`. 

> We split the list in half and solve each recursively.
> For the base case, the list length is 1. We either return Result(1, 1, 1, True) or Result(0, 0, 0, False), depending on if the input is equal to the key.
> The main difficulty is in combining the results of the two recursive calls. To do so, we need to take the Result objects from each recursive call, and combine them together to make a new Result object. To do so, we have to take the max of the left side and right side. But, we also have to consider cases where the longest sequence spans the two sides. E.g., if the key is `12` and the two sides are `[6 12] [12 6] -> [6 12 12 6]`. Here, the longest sequence of 12s requires adding together `result1.right_side` and `result2.left_side`.
> 
> I'd recommend walking through a number of examples to work out the logic. A good test case to check is `assert to_value(longest_run_recursive([6, 12, 12, 12, 12, 6, 6, 6], 12)) == 4`

```python

class Result:
    """ done """
    def __init__(self, left_size, right_size, longest_size, is_entire_range):
        self.left_size = left_size               # run on left side of input
        self.right_size = right_size             # run on right side of input
        self.longest_size = longest_size         # longest run in input
        self.is_entire_range = is_entire_range   # True if the entire input matches the key
        
    def __repr__(self):
        return('longest_size=%d left_size=%d right_size=%d is_entire_range=%s' %
              (self.longest_size, self.left_size, self.right_size, self.is_entire_range))
    

def longest_run_recursive(mylist, key):    
    ### TODO
    return _longest_run_recursive(mylist, key).longest_size
    ###

def _longest_run_recursive(mylist, key):
    # returns Result object
    if len(mylist) == 1:
        if mylist[0] == key:            
            return Result(1, 1, 1, True)
        else:
            return Result(0, 0, 0, False)
    
    # each thread spawns more threads
    result1 = _longest_run_recursive(mylist[:len(mylist)//2], key)
    result2 = _longest_run_recursive(mylist[len(mylist)//2:], key)
    return combine_results(result1, result2)
    ###

def combine_results(result1, result2):
    res = None
    if result1.is_entire_range and result2.is_entire_range:
        total = result1.longest_size + result2.longest_size
        return Result(total, total, total, True)
    else:
        left_size = result1.left_size
        if result1.is_entire_range:  # e.g., [12 12] [12 6] -> [12 12 12 6]
            left_size += result2.left_size

        right_size = result2.right_size
        if result2.is_entire_range:  # e.g., [6 12] [12 12] -> [6 12 12 12]
            right_size += result1.right_size

        overlap = result1.right_size + result2.left_size

        return Result(
            left_size,
            right_size,
            max(overlap, result1.longest_size, result2.longest_size),
            False
        )
```



  - 3d. What is the Work and Span of this sequential algorithm?

> Since we split into two problems, each half the original size, and it takes constant time to merge the results, we get work:

$W(n) = 2W(n/2) + 1$  

We can solve with the brick method -- leaf dominated. Height of tree is $\lg n$, number of leaves is $2^{\lg n}$, so $O(n)$.

Span is same as above, since it is *sequential*.  


  - 3e. Assume that we parallelize in a similar way we did with `sum_list_recursive`. That is, each recursive call spawns a new thread. What is the Work and Span of this algorithm?

Work is same as above.

Since it is parallel, the span recurrence is

$S(n) = S(n/2) + 1$

Using the brick method, this is *balanced*. The worst level is $1$ and the number of levels is $\lg n$. Multiplying those together, we get $O(\lg n)$


