Yes — that’s the idiomatic Python design.

Here’s the distilled rule:

# ✅ **In Python, functions should *raise* early and let the *caller* decide what to do.**

You normally **don't** accumulate errors inside a low-level function.
Instead:

* **Fail fast** inside the function (`raise`)
* **Handle/log** in the *outermost layer* (your `main`, your API endpoint, your CLI command, etc.)

This separation makes your code cleaner, easier to test, easier to reason about, and avoids double-logging.

---

# 🔍 Why this is the Pythonic approach

### **1. Avoids mixing concerns**

The function `calculator()` should “do the math” — not do accounting of error states.

### **2. No silent failures**

Returning `None` or accumulating errors hides failures.

Python philosophy: *errors should never pass silently* (unless explicitly handled).

### **3. One place for logging**

Logging in a single top-level place avoids:

* duplicates
* partial context
* scattered log statements everywhere

### **4. Clean call sites**

Anything calling `calculator()` knows exactly when something failed.

---

# 🧠 A good way to think about it

### **Low-level functions should raise.**

### **High-level code decides how to react to failure.**

In your application:

```
to_float → raises
calculator → raises
main() → catches + logs
```

Execution flow is crystal clear.

---

# 🧱 Your resulting structure

**calculator.py**

```python
def calculator(a, b, operator):
    a = to_float(a)
    b = to_float(b)

    if operator not in (...):
        raise InvalidOperatorError(operator)

    match operator:
        case "add": return a + b
        case "subtract": return a - b
        case "multiply": return a * b
        case "divide":
            if b == 0:
                raise DivisionByZeroError(a, b)
            return a / b
```

**main.py**

```python
def main():
    try:
        result = calculator("hello", 10, "add")
    except (InvalidInputError, InvalidOperatorError, DivisionByZeroError) as e:
        logger.error("Calculation failed: %s", e, exc_info=True)
        return

    print("Result:", result)
```

---

# TL;DR

✔️ **Yes — don’t accumulate errors in `calculator()`.**
✔️ **Let exceptions abort the function immediately.**
✔️ **Catch + log once at the top-level (main, API, CLI).**
✔️ **This is the clean, Pythonic, maintainable pattern.**

If you want, I can also show:

* a version that returns a structured result (`Result | Error`)
* or a version that accumulates errors *intentionally* (rare, but useful for validation libraries)

Just say the word.
