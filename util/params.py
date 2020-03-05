class Params:
    penalty_same_color = 10  # penalty for same color edges
    penalty_per_color_used = 1  # penalty for using extra colours
    multiplier = 1
    initial_population_size = 5 * multiplier
    crossover_parents = 3 * multiplier
    mutation_parents = 10 * multiplier
    random_count = 3 * multiplier

    propogation_count = 50 * multiplier
    stop_genetic_after_count = 10
    #no_colours = 8
    mutation_function = "4"
    crossover_function = "Jumbled"

    @staticmethod
    def set_penalty_same_color(new_penalty_same_color):
        Params.penalty_same_color = new_penalty_same_color

    @staticmethod
    def set_penalty_per_color_used(new_penalty_per_color_used):
        Params.penalty_per_color_used = new_penalty_per_color_used

    @staticmethod
    def set_multiplier(new_multiplier):
        Params.multiplier = new_multiplier

    @staticmethod
    def set_initial_population_size(new_initial_population_size):
        Params.initial_population_size = new_initial_population_size

    @staticmethod
    def set_crossover_parents(new_crossover_parents):
        Params.crossover_parents = new_crossover_parents

    @staticmethod
    def set_mutation_parents(new_mutation_parents):
        Params.mutation_parents = new_mutation_parents

    @staticmethod
    def set_random_count(new_random_count):
        Params.random_count = new_random_count

    @staticmethod
    def set_propogation_count(new_propogation_count):
        Params.propogation_count = new_propogation_count

    @staticmethod
    def set_stop_genetic_after_count(new_stop_genetic_after_count):
        Params.stop_genetic_after_count = new_stop_genetic_after_count

    @staticmethod
    def set_no_colours(new_no_colours):
        Params.no_colours = new_no_colours

    @staticmethod
    def set_mutation_function(new_mutation_function):
        Params.mutation_function = new_mutation_function

    @staticmethod
    def set_crossover_function(new_crossover_function):
        Params.crossover_function = new_crossover_function
