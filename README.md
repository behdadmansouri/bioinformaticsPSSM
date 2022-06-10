# PSSM builder, query matcher
#### How to run
1. Enter `N`, the number of sequences you want to build the PSSM from
2. Enter the said  `N`sequences
3. Enter the query

Example 1:
```
4
HVLIP
H-MIP
HVL-P
LVLIP
LIVPHHVPIPVLVIHPVLPPHIVLHHIHVHIHLPVLHIVHHLVIHLHPIVL
```
Output 1:
```
H-L-P
```
Example 2:
```
4
T-CT
--CT
A-CT
ATCT
ATCCTATATCTTCTCTATACTATCCTTCA
```
Output 2:
```
A-CT
```
You can run these examples as tests by uncommenting `test()` at the end of the file.
```python
# uncomment test() to test the code
# test()
```