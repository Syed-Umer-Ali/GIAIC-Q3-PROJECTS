import streamlit as st

st.title("🌀 Fibonacci Calculator")

# Fibonacci Function
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


n = st.number_input("Enter a non-negative integer:", min_value=0, step=1, format="%d")

# Button to Calculate Fibonacci
if st.button("Calculate Fibonacci"):
    result = fibonacci(n)
    st.success(f"The {n}th Fibonacci number is {result}")

    
st.markdown("""
---

# 📖 Fibonacci Sequence info
The **Fibonacci Sequence** is a mathematical sequence where each number is the **sum of the two preceding numbers**.

## 🔢 Fibonacci Series:
`0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, …`

## 📌 Formula:
\[
F(n) = F(n-1) + F(n-2)
\]
Where:  
- **F(0) = 0**  
- **F(1) = 1**  
- **F(2) = 1** (0 + 1)  
- **F(3) = 2** (1 + 1)  
- **F(4) = 3** (1 + 2)  
- **F(5) = 5** (2 + 3)  
- **F(6) = 8** (3 + 5)  
And so on...
""")
