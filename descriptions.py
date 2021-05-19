list_input = {"-": "-",
              "Spot price": "Current market price at which asset is bought or sold.",

              "Strike": 'The price at which a put or call option can be exercised.',

              "Risk-free rate": 'The risk-free interest rate is the rate of return of a hypothetical investment with no'
                                ' risk of financial loss, over a given period of time.',

              "Volatility": 'Standard deviation of the underlying asset stock price, in other words the degree of'
                            ' variation of the price.',

              "Maturity": 'Date on which the option will cease to exist, and when the investor will be able to exercise'
                          ' his right to buy or sell the underlying asset).',

              "Drift": 'Rate at which the underlying stock average changes. It gives the general trend of the stock '
                       'movements.',

              "Discretization step": 'Used in the pricing model of the underlying asset, its mathematical definition is'
                                     ' the step at which the continuous period (i.e. from t = 0 to t = maturity) is'
                                     ' discretized. Financially speaking, it is time between each pricing of the asset.',

              "Tree periods": "Size of the binomial lattice (tree). 10-20 are more than enough to converge to the "
                              "Black-Scholes price. The number of nodes for a given lattice of n periods is given by an"
                              " arithmetic progression with common  difference between terms of 1, i.e. "
                              "\(S = \\frac{s_1+s_n}{2}n\)",
              "Rebalancing frequency": "Frequency of replication strategy portfolio rebalancing relative to the "
                                       "discretization step. If equal to 1, the portfolio will be rebalanced at every"
                                       " discretization step. If equal to two, the portfolio will be rebalanced every 2"
                                       " discretization steps, ... The higher, the lower the quality of the replication"
                                       " strategy. It is best left at 1 if looking for the best replication strategy. "
                                       "Min = 1 (rebalanced every  discretization step) ; "
                                       "Max = Maturity / Discretization step (rebalanced once, at maturity)",

              "Number of simulations": "Number of replication strategies to be computed. Maximum 10.",

              "Transaction costs": "Transaction costs are expenses incurred when buying or selling the underlying "
                                   "asset. Can be fixed or proportional to the number of underlying asset bought or "
                                   "sold. Typically a few basis points, i.e. less than a tenth of a percentage. Given"
                                   " the Black-Scholes model assumptions, where transactions costs are null, "
                                   "considering them will decrease the quality of the replication strategy."
              }
