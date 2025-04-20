# PLL_survey
A repository of the most recent published PLLs, with various performance comparison graphs.

For example, the following graph is comparing fractional PLLs based on their FOM and worst fractional spur level highlighting differences in area, oscillator type, and PLL type. \
(The highlighted point is just an example to show how you can compare your design against other references.)
![Spur FOM example](./Spur_FOM.svg)



## Cite this survey
It is all free and with a permisssive license to use this repository in any form. We just kindly ask you to reference it in your work to encourage the authors for more contributions.

For citation use this information: \
Parham Davami, "Phase-Locked Loops (PLL) Performance Survey", [online]. Available: https://github.com/Parhamdada/PLL_survey

## Usage
For using this repository you need to have [python](https://www.python.org/) installed. Then you may clone or download the repository, and run the python code with command `python pll_survey.py`. \
If you want to compare your design with other references, adapt the first input line of `pll_data.csv` file and run the python code.

### Data item guide
* Remove the items in the plot by setting its corresponding plot flag to 'FALSE'.
* Integer PLLs have empty fractional spur column.


## Contributions
This repo needs ***YOU***. With your collaboration we can make this repo more impactful.

For contributions, please;
1. make a new branch with a name like `ENH/additional_references` (TAGs can be: `FEAT` for a feature in code like a new comparison graph, `ENH` for additional references, `BUG` for correcting something wrong somewhere (even here!))
2. Create a pull request to the main branch, your branch will be merged to the main branch after a compatibility review.
3. Your name will be added to the authors' list for future citations.


If you face a bug or need a feature but you don't have the bandwidth to implement it yourself, please open an issue item with a discription and it will be handled by the contributors.