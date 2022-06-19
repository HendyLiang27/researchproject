import pandas as pd

data = pd.read_csv('all_data.csv')
slark_data = pd.read_csv('all_data_slark.csv')
slark_data['slark'] = True
complete = pd.merge(data, slark_data, how='left').fillna(False)
prob_slark = len(slark_data) / len(data)
prob_not_slark = 1 - prob_slark
prob_win_given_hurricane_pike = len(complete[(complete['win'] & complete['enemy_bought_hurricane_pike'])]) / len(complete[complete['enemy_bought_hurricane_pike']])
prob_win_given_not_hurricane_pike = len(complete[(complete['win'] & complete['enemy_bought_hurricane_pike'].eq(False))]) / len(complete[complete['enemy_bought_hurricane_pike'].eq(False)])
prob_win_given_slark_and_hurricane_pike = len(slark_data[(slark_data['win']) & slark_data['enemy_bought_hurricane_pike']]) \
                                          / len(slark_data[slark_data['enemy_bought_hurricane_pike']])
prob_win_given_not_slark_and_hurricane_pike = len(complete[(complete['win'] & complete['slark'].eq(False) & complete['enemy_bought_hurricane_pike'])]) \
                                              / len(complete[complete['enemy_bought_hurricane_pike'] & complete['slark'].eq(False)])
prob_win_given_not_slark_and_not_hurricane_pike = len(complete[(complete['win'] & complete['slark'].eq(False) & complete['enemy_bought_hurricane_pike'].eq(False))]) \
                                                 / len(complete[complete['enemy_bought_hurricane_pike'].eq(False) & complete['slark'].eq(False)])
prob_win_given_slark_and_not_hurricane_pike = len(slark_data[(slark_data['win']) & slark_data['enemy_bought_hurricane_pike'].eq(False)]) \
                                              / len(slark_data[slark_data['enemy_bought_hurricane_pike'].eq(False)])
prob_hurricane_pike_given_slark = len(slark_data[slark_data['enemy_bought_hurricane_pike']]) / len(slark_data)
prob_not_hurricane_pike_given_slark = len(slark_data[slark_data['enemy_bought_hurricane_pike'].eq(False)]) / len(slark_data)
prob_hurricane_pike_given_not_slark = len(complete[(complete['enemy_bought_hurricane_pike']) & complete['slark'].eq(False)]) \
                                      / len(complete[complete['slark'].eq(False)])
prob_not_hurricane_pike_given_not_slark = len(complete[(complete['enemy_bought_hurricane_pike'].eq(False)) & complete['slark'].eq(False)]) \
                                      / len(complete[complete['slark'].eq(False)])
print('probability P(Slark) =', prob_slark)
print('probability P(¬Slark) =', prob_not_slark)
print('probability P(Win|Hurricane Pike, Slark) * P(Slark) =', prob_win_given_slark_and_hurricane_pike * prob_slark)
print('probability P(Win|Hurricane Pike, ¬Slark) * P(¬Slark) =', prob_win_given_not_slark_and_hurricane_pike * prob_not_slark)
print('probability P(Win|Hurricane Pike) =', prob_win_given_hurricane_pike)
print('probability P(Win|¬Hurricane Pike) =', prob_win_given_not_hurricane_pike)
print('probability P(Hurricane Pike|Slark) =', prob_hurricane_pike_given_slark)
print('probability P(Hurricane Pike|¬Slark) =', prob_hurricane_pike_given_not_slark)
print('probability P(¬Hurricane Pike|Slark) =', prob_not_hurricane_pike_given_slark)
term1do = prob_hurricane_pike_given_slark * prob_win_given_slark_and_hurricane_pike * prob_slark
term2do = prob_not_hurricane_pike_given_slark * prob_win_given_slark_and_not_hurricane_pike * prob_slark
term3do = prob_hurricane_pike_given_slark * prob_win_given_not_slark_and_hurricane_pike * prob_not_slark
term4do = prob_not_hurricane_pike_given_slark * prob_win_given_not_slark_and_not_hurricane_pike * prob_not_slark
print('scenario (Hurricane Pike, Slark) = ', term1do)
print('scenario (¬Hurricane Pike, Slark) = ', term2do)
print('scenario (Hurricane Pike, ¬Slark) = ', term3do)
print('scenario (¬Hurricane Pike, ¬Slark) = ', term4do)
front_door_criterion_do_slark = term1do + term2do + term3do + term4do
term1dont = prob_hurricane_pike_given_not_slark * prob_win_given_slark_and_hurricane_pike * prob_slark
term2dont = prob_not_hurricane_pike_given_not_slark * prob_win_given_slark_and_not_hurricane_pike * prob_slark
term3dont = prob_hurricane_pike_given_not_slark * prob_win_given_not_slark_and_hurricane_pike * prob_not_slark
term4dont = prob_not_hurricane_pike_given_not_slark * prob_win_given_not_slark_and_not_hurricane_pike * prob_not_slark
front_door_criterion_do_not_slark = term1dont + term2dont + term3dont + term4dont
print('STEP ONE FDC: probability P(Hurricane Pike|Slark) =', prob_hurricane_pike_given_slark)
print('STEP TWO FDC: probability ΣSlark P(Win|Hurricane Pike, Slark) P(Slark) =', prob_win_given_slark_and_hurricane_pike * prob_slark + prob_win_given_not_slark_and_hurricane_pike * prob_not_slark)
print('STEP THREE FDC: probability P(Slark|do(Win) =', front_door_criterion_do_slark)
print('probability P(Slark|do(¬Win) =', front_door_criterion_do_not_slark)
print('ATE = ', (front_door_criterion_do_slark - front_door_criterion_do_not_slark) * 100, '%')

print('--------------------------------------------')
print('Stats')
print('games =',len(complete))
print('wins =', len(complete[complete['win']]))
print('slark picked =', len(slark_data))
print('slark not picked =', len(complete[complete['slark'].eq(False)]))
print('enemy hurricane pike bought =', len(complete[complete['enemy_bought_hurricane_pike']]))
print('slark wins = ', len(slark_data[slark_data['win']]))
print('slark not picked wins =', len(complete[complete['slark'].eq(False) & complete['win']]))
print('enemy hurricane pike bought when slark =', len(slark_data[slark_data['enemy_bought_hurricane_pike']]))
print('enemy hurricane pike bought when not slark =', len(complete[complete['enemy_bought_hurricane_pike'] & complete['slark'].eq(False)]))

def calculate_ace(seed):
    sample = complete.sample(len(complete), random_state=seed, replace=True)
    prob_win_given_slark_and_hurricane_pike = len(sample[(sample['win']) & sample['enemy_bought_hurricane_pike'] & sample['slark']]) \
                                              / len(sample[sample['enemy_bought_hurricane_pike'] & sample['slark']])
    prob_win_given_not_slark_and_hurricane_pike = len(sample[(sample['win'] & sample['slark'].eq(False) & sample['enemy_bought_hurricane_pike'])]) \
                                                  / len(sample[sample['enemy_bought_hurricane_pike'] & sample['slark'].eq(False)])
    prob_win_given_not_slark_and_not_hurricane_pike = len(sample[(sample['win'] & sample['slark'].eq(False) & sample['enemy_bought_hurricane_pike'].eq(False))]) \
                                                      / len(sample[sample['enemy_bought_hurricane_pike'].eq(False) & sample['slark'].eq(False)])
    prob_win_given_slark_and_not_hurricane_pike = len(sample[(sample['win']) & sample['enemy_bought_hurricane_pike'].eq(False) & sample['slark']]) \
                                                  / len(sample[sample['enemy_bought_hurricane_pike'].eq(False) & sample['slark']])
    prob_hurricane_pike_given_slark = len(sample[sample['enemy_bought_hurricane_pike'] & sample['slark']]) / len(sample[sample['slark']])
    prob_not_hurricane_pike_given_slark = len(sample[sample['enemy_bought_hurricane_pike'].eq(False) & sample['slark']]) / len(sample[sample['slark']])
    prob_hurricane_pike_given_not_slark = len(sample[(sample['enemy_bought_hurricane_pike']) & sample['slark'].eq(False)]) \
                                          / len(sample[sample['slark'].eq(False)])
    prob_not_hurricane_pike_given_not_slark = len(sample[(sample['enemy_bought_hurricane_pike'].eq(False)) & sample['slark'].eq(False)]) \
                                              / len(sample[sample['slark'].eq(False)])
    term1do = prob_hurricane_pike_given_slark * prob_win_given_slark_and_hurricane_pike * prob_slark
    term2do = prob_not_hurricane_pike_given_slark * prob_win_given_slark_and_not_hurricane_pike * prob_slark
    term3do = prob_hurricane_pike_given_slark * prob_win_given_not_slark_and_hurricane_pike * prob_not_slark
    term4do = prob_not_hurricane_pike_given_slark * prob_win_given_not_slark_and_not_hurricane_pike * prob_not_slark
    front_door_criterion_do_slark = term1do + term2do + term3do + term4do
    term1dont = prob_hurricane_pike_given_not_slark * prob_win_given_slark_and_hurricane_pike * prob_slark
    term2dont = prob_not_hurricane_pike_given_not_slark * prob_win_given_slark_and_not_hurricane_pike * prob_slark
    term3dont = prob_hurricane_pike_given_not_slark * prob_win_given_not_slark_and_hurricane_pike * prob_not_slark
    term4dont = prob_not_hurricane_pike_given_not_slark * prob_win_given_not_slark_and_not_hurricane_pike * prob_not_slark
    front_door_criterion_do_not_slark = term1dont + term2dont + term3dont + term4dont
    return front_door_criterion_do_slark - front_door_criterion_do_not_slark


aces = []
# Bootstrap with 1000 iterations
n_iterations = 1000
for i in range(n_iterations):
    # using the index as a random seed for sampling
    aces.append(calculate_ace(i))
aces.sort()

print('ATE = ', (front_door_criterion_do_slark - front_door_criterion_do_not_slark))
print('95% confidence interval(', aces[25], '<', aces[500], '<', aces[975], ')')





