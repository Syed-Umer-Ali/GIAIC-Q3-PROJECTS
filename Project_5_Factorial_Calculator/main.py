import streamlit as st
import math 


st.title("⚡ Factorial Calculator")

# Factorial Function
def factorial(n):
    return math.factorial(n) 


n = st.number_input("Enter a non-negative integer:", min_value=0, step=1, format="%d")

# Button to Calculate Factorial
if st.button("Calculate Factorial"):
    result = factorial(n)
    st.success(f"The factorial of {n} is {result}")

st.markdown("""
---
# What is Factorial?
# 🔢 Factorial (n!)
Factorial of a number **n** (denoted as **n!**) is the **product of all positive integers from 1 to n**.

## 📌 Formula:
\[
n! = n \times (n-1) \times (n-2) \times ... \times 2 \times 1
\]

### ✅ Examples:
- **5! = 5 × 4 × 3 × 2 × 1 = 120**  
- **4! = 4 × 3 × 2 × 1 = 24**  
- **1! = 1**  
- **0! = 1** (By definition)  

## 💡 Real-Life Applications of Factorial
1. **Mathematics & Combinatorics:** Used in probability, permutations, and combinations.  
2. **Computer Science:** Applied in recursive algorithms and complexity analysis.  
3. **Physics:** Used in statistical mechanics and quantum physics.  
4. **Machine Learning & AI:** Factorial-based formulas appear in probabilistic models.
""")
