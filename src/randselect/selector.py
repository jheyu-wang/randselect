import random

def random_selection(n_list, q_list, rng=random):

  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name, chosen_question)


def available_choices(pool, used):
  remaining = [item for item in pool if item not in used]
  return remaining if remaining else list(pool)