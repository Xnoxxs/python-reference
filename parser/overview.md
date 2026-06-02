# Parser

A parser is a Python tool that reads **command-line arguments** — the extra text you type after a script name in the terminal — and turns it into values your program can use.

## Example in this folder

[`parser.py`](example.py) is a minimal example. Run it from `backend/`:

```bash
python parser/example.py --name Hamza
```

What happens:

1. Python executes `parser/parser.py`.
2. The parser captures the flag `--name` and its value `Hamza`.
3. The script prints that value.

Output:

```
Hamza
```

---

# Example 2 — Default Value

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--country",
    default="Morocco"
)

args = parser.parse_args()

print(args.country)
```

Run without anything:

```bash
python test.py
```

Output:

```txt
Morocco
```

Override it:

```bash
python test.py --country Spain
```

Output:

```txt
Spain
```

---

# Example 3 — Required Argument

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--email",
    required=True
)

args = parser.parse_args()

print(args.email)
```

Run without email:

```bash
python test.py
```

Output:

```txt
error: the following arguments are required: --email
```

---

# Example 4 — Integer Type

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--age",
    type=int
)

args = parser.parse_args()

print(args.age + 5)
```

Run:

```bash
python test.py --age 20
```

Output:

```txt
25
```

`type=int` automatically converts:

```txt
"20"
```

into:

```python
20
```

(real integer)

---

# Example 5 — Boolean Flag

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug",
    action="store_true"
)

args = parser.parse_args()

print(args.debug)
```

Run without flag:

```bash
python test.py
```

Output:

```txt
False
```

Run with flag:

```bash
python test.py --debug
```

Output:

```txt
True
```

Very commonly used for:

* `--dry-run`
* `--commit`
* `--verbose`
* `--debug`

---

# Example 6 — Help Menu

```python
import argparse

parser = argparse.ArgumentParser(
    description="Create a new user"
)

parser.add_argument(
    "--name",
    help="Name of the user"
)

parser.parse_args()
```

Run:

```bash
python test.py --help
```

Output:

```txt
usage: test.py [-h] [--name NAME]

Create a new user

options:
  -h, --help   show this help message and exit
  --name NAME  Name of the user
```

---

# Understanding parser.add_argument()

Example:

```python
parser.add_argument(
    "--config",
    type=str,
    default="config.yaml",
    help="Path to config file",
    required=False
)
```

## What Each Part Means

| Part        | Meaning                            |
| ----------- | ---------------------------------- |
| `--config`  | Command-line flag                  |
| `type=str`  | Converts input into a string       |
| `default=`  | Used if user doesn't provide value |
| `help=`     | Appears in `--help` menu           |
| `required=` | Forces user to provide argument    |

---

# Big Picture

`argparse` basically lets you create:

```txt
mini terminal APIs
```

for your Python scripts.

You define:

* flags
* types
* defaults
* requirements

Then Python automatically handles:

* parsing
* validation
* errors
* help menus
