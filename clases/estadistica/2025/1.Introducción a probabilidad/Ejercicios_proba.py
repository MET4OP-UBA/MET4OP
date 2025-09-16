#%% [markdown]
# # Probability Exercises for University Students
# 

#%% [markdown]
# ## Part 1: Foundational Concepts
# ---
# 
# ### Title: Basic Probability and Independence (Handedness)
# **1.** About 9% of people are left-handed. Suppose 2 people are selected at random from the U.S. population. Because the sample size of 2 is very small relative to the population, it is reasonable to assume these two people are independent. 
# (a) What is the probability that both are left-handed?
# (b) What is the probability that both are right-handed?
# 
# ---
# 
# ### Title: Product and Complement Rule (Handedness)
# **2.**
# Suppose 5 people are selected at random.
# (a) What is the probability that all are right-handed?
# (b) What is the probability that all are left-handed?
# (c) What is the probability that not all of the people are right-handed? 
# 
# ---
# 
# ### Title: Product Rule under Independence (Sex and Handedness)
# **3.** Suppose the variables handedness and sex are independent. We know that P(right-handed) = 0.91 and P(female) = 0.50.
# 
# Three people are selected at random.
# (a) What is the probability that the first person is male and right-handed?
# (b) What is the probability that the first two people are male and right-handed?.
# (c) What is the probability that the third person is female and left-handed?
# (d) What is the probability that the first two people are male and right-handed and the third person is female and left-handed? 
# 
# ---
# 
# ### Title: Sets, Venn Diagrams, and Independence (Swing Voters)
# **4.**
# A Pew Research survey found that 35% of registered voters identify as Independent, 23% identify as swing voters, and 11% identify as both.
# (a) Are being Independent and being a swing voter disjoint (mutually exclusive)? 
# (b) Draw a Venn diagram summarizing the probabilities. 
# (c) What percent of voters are Independent but not swing voters? 
# (d) What percent of voters are Independent or swing voters? 
# (e) What percent of voters are neither Independent nor swing voters? 
# (f) Is the event that someone is a swing voter independent of the event that someone is an Independent? 
# 
# ---
# 
# ### Title: Permutations and Arrangements (Parking)
# **5.** A small company has five employees: Anna, Ben, Carl, Damian, and Eddy, and five unassigned parking spots in a row. All possible parking arrangements are equally likely. 
# (a) On a given day, what is the probability that the employees park in alphabetical order? 
# (b) How many total ways are there to arrange the five cars? 
# (c) Now consider 8 employees. How many possible ways are there to order their cars?

#%% [markdown]
# ## Part 2: Discrete Probability Distributions
# ---

#%% [markdown]
# ### Section: The Bernoulli Distribution
# *A Bernoulli trial is a single experiment with exactly two possible outcomes: "success" or "failure". It's the fundamental building block for other discrete distributions.*
# 
# **B1. (Civic Engagement SMS)**
# A city sends a public service announcement (PSA) via SMS. The probability that a citizen reads the message is $p = 0.35$.
# Let $X$ be a random variable where $X=1$ if the message is read and $X=0$ otherwise.
# 
# (a) State the probability mass function (PMF) for $X$. Calculate $P(X=1)$ and $P(X=0)$.
# (b) Calculate the expected value, $E[X]$, and the variance, $Var(X)$.
# (c) **Interpret** the meaning of $E[X]$ in this context.
# 
# **B2. (Voter Turnout Survey)**
# A pollster calls a registered voter. The probability of the person confirming they voted in the last election is $p = 0.6$. Let $Y$ be the Bernoulli random variable for this outcome.
# 
# (a) Define the "success" and "failure" for this trial and their probabilities.
# (b) If the pollster makes 100 such calls, what is the expected number of people who will confirm they voted? How does this relate to $E[Y]$?

#%% [markdown]
# ### Section: The Geometric Distribution
# *The Geometric distribution models the number of Bernoulli trials needed to get the first success.*
# 
# **G1. (First Undecided Voter)**
# In a phone poll, the probability of reaching an undecided voter is $p = 0.2$. Let $T$ be the number of calls made until the first undecided voter is found.
# 
# (a) What is the probability that the first undecided voter is the 3rd person called? ($P(T=3)$).
# (b) What is the probability that it takes **more than 4** calls to find an undecided voter?
# (c) What is the expected number of calls needed?
# 
# **G2. (First Official Response)**
# An investigative journalist sends emails to public officials. The probability of getting a response is $p = 0.05$. Let $R$ be the number of emails sent until the first response.
# 
# (a) Calculate the probability that the first response is received on the 10th email, $P(R=10)$.
# (b) What is the probability of getting the first response within the first 3 emails, $P(R \le 3)$?
# (c) What is the expected number of emails the journalist needs to send to get one response?

#%% [markdown]
# ### Section: The Binomial Distribution
# *The Binomial distribution models the number of successes in a fixed number of independent Bernoulli trials.*
# 
# **N1. (Forum Attendance)**
# A city council sends 20 invitations to a public forum. Each person attends with a probability of $p = 0.25$, independently. Let $X$ be the number of attendees.
# 
# (a) Justify why $X$ follows a Binomial distribution, $X \sim Bin(n=20, p=0.25)$.
# (b) Calculate the probability that **exactly 5** people attend, $P(X=5)$.
# (c) Calculate the probability that **at least 3** people attend, $P(X \ge 3)$.
# (d) Calculate the expected number of attendees, $E[X]$, and the standard deviation, $SD(X)$.
# 
# **N2. (Social Media Sharing)**
# An informative graphic is shown to 12 people. The probability that any one person shares it is $p = 0.15$, independently. Let $Y$ be the number of shares.
# 
# (a) What is the probability that **no one** shares the graphic, $P(Y=0)$?
# (b) What is the probability that it's shared by **two or more** people, $P(Y \ge 2)$?
# (c) What does $E[Y]$ signify for the communications team?

#%% [markdown]
# ### Section: The Poisson Distribution
# *The Poisson distribution models the number of events occurring in a fixed interval of time or space, given a constant average rate.*
# 
# **P1. (Helpline Calls)**
# An election helpline receives an average of $\lambda = 4$ calls per hour. Assume a Poisson process. Let $X$ be the number of calls in one hour.
# 
# (a) What is the probability of receiving **exactly 0** calls in a given hour?
# (b) What is the probability of receiving **3 or more** calls in a given hour?
# (c) What is the probability of receiving **at least one** call in a 30-minute interval? (Hint: Adjust $\lambda$).
# 
# **P2. (Citizen Infrastructure Reports)**
# A municipal app receives reports at an average rate of $\lambda = 18$ per day.
# 
# (a) What is the probability of receiving **exactly 20** reports on a given day?
# (b) What is the probability of receiving **at most 15** reports, $P(X \le 15)$?
# (c) What is the expected number of reports in an 8-hour workday?

#%% [markdown]
# ## Part 3: Continuous Distributions & Bayes' Theorem Revisited
# ---

#%% [markdown]
# ### Section: The Normal Distribution
# *The Normal distribution is a continuous probability distribution that is symmetrical on both sides of the mean, showing that data near the mean are more frequent in occurrence than data far from the mean.*
# 
# **ND1. Area under the curve, Part I.** What percent of a standard normal distribution $N(\mu = 0, \sigma = 1)$ is found in each region? Be sure to draw a graph for each.
# 
# (a) $Z < -1.35$
# (b) $Z > 1.48$
# (c) $-0.4 < Z < 1.5$
# (d) $|Z| > 2$
# 
# **ND2. Area under the curve, Part II.** What percent of a standard normal distribution $N(\mu = 0, \sigma = 1)$ is found in each region? Be sure to draw a graph for each.
# 
# (a) $Z > -1.13$
# (b) $Z < 0.18$
# (c) $Z > 8$
# (d) $|Z| < 0.5$
# 
# **ND3. Election Performance Analysis.** In political science, it's common to compare election results across different districts or states. Two candidates from "Party X" ran for governor in two different states. Candidate Smith ran in State A, a traditional stronghold for the party, while Candidate Jones ran in State B, a highly competitive "swing" state.
# 
# Smith won with 63% of the vote in State A, while Jones won with a smaller majority of 54% in State B. They are curious about who had the more impressive victory relative to their state's political landscape. Here is some historical data:
# 
# - The vote shares for Party X's gubernatorial candidates in **State A** follow a normal distribution with a mean of 58% and a standard deviation of 4%.
# - The vote shares for Party X's gubernatorial candidates in **State B** follow a normal distribution with a mean of 47% and a standard deviation of 6%.
# - Remember: a better performance corresponds to a higher vote share.
# 
# (a) Write down the shorthand for these two normal distributions.
# (b) What are the Z-scores for Smith's and Jones's results? What do these Z-scores tell you?
# (c) Did Smith or Jones perform better relative to their respective states? Explain your reasoning.
# (d) What percent of historical candidates in State A did Smith outperform?
# (e) What percent of historical candidates in State B did Jones outperform?
# (f) If the distributions of vote shares were not nearly normal, would your answers to parts (b) - (e) change? Explain your reasoning.

#%% [markdown]
# ### Section: Bayes' Theorem
# *Bayes' Theorem helps us update our beliefs about a probability based on new evidence.*
# 
# **Y1. (Civic Message Classifier)**
# 30% of incoming messages are "civic-related" (C), so $P(C) = 0.30$. A machine learning model has:
# - A **sensitivity** of 0.90: $P(\text{Positive} | C) = 0.90$
# - A **specificity** of 0.80: $P(\text{Negative} | \neg C) = 0.80$
# 
# (a) A message is classified as "Positive". What is the posterior probability that it is actually civic-related, $P(C | \text{Positive})$?
# (b) If a message is classified as "Negative", what is the probability that it was actually civic-related (a false negative), $P(C | \text{Negative})$?
# 
# **Y2. (Voter Registration Verification)**
# 5% of records have a significant error (E), so $P(E) = 0.05$. An algorithm flags suspicious records with the following performance:
# - It correctly identifies 95% of records with errors: $P(S | E) = 0.95$
# - It incorrectly flags 2% of correct records: $P(S | \neg E) = 0.02$
# 
# (a) A record is flagged as suspicious. What is the probability it actually has an error, $P(E | S)$?
# (b) What is the probability a record has an error even if it was **not** flagged, $P(E | \neg S)$?
# (c) **Interpret** the result from (a). Is the flag a reliable indicator of an error?
# 
# **Y3. Predisposition for Thrombosis.** A genetic test is used to determine if people have a predisposition for thrombosis. It is believed that 3% of people actually have this predisposition. The genetic test is 99% accurate if a person actually has the predisposition (i.e., the probability of a positive test given the predisposition is 0.99). The test is 98% accurate if a person does not have the predisposition. What is the probability that a randomly selected person who tests positive for the predisposition by the test actually has the predisposition?
# 
# **Y4. It’s Never Lupus.** Lupus is a disease where it is believed that 2% of the population suffer from it. A test for lupus is 98% accurate if a person actually has the disease. The test is 74% accurate if a person does not have the disease. There is a line from the TV show *House*: “It’s never lupus.” Do you think there is truth to this statement? Use the probability that a person who tests positive actually has lupus to support your answer.
# 
# **Y5. Exit Poll Analysis.** An exit poll found that 53% of respondents voted for Candidate A. Additionally, they estimated that of those who voted for Candidate A, 37% had a college degree. Of those who voted against Candidate A, 44% had a college degree. Suppose we randomly sample a person from the exit poll and they have a college degree. What is the probability they voted for Candidate A?