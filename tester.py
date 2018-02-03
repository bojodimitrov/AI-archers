from player import SmartPlayer
import neural_networks as nn
import physics_consts

TEST_TRIALS_NUMBER = 100

class TrialTester:
    def __init__(self, location, target_location):
        self.test_archer = SmartPlayer(location)
        self.best_player_ref = None
        self.gravity = None
        self.test_trials = 1
        self.target_location = target_location
        self.test_results = [0, 0]

    def evaluate_test_archer_shot(self, rain, wind):
        self.test_archer.set_neural_network(self.best_player_ref.get_neural_network())
        result = self.test_archer.get_neural_network().feed_forward(
                [self.target_location[0] - self.test_archer.player_x,
                 self.target_location[1] - self.test_archer.player_y,
                 self.gravity,
                 rain,
                 wind[0],
                 wind[1]],
                nn.f.identity)
        self.test_archer.shoot([result[0], result[1]], result[2])

    def archer_tried(self):
        return self.test_archer.waiting

    def tests_finished(self):
        return self.test_trials % TEST_TRIALS_NUMBER == 0

    def reset(self):
        self.test_results = [0, 0]
        self.test_trials = 1

    def get_test_results(self):
        return self.test_results

    def test_best_archer(self, canvas):
        if self.test_archer.hitted == 1:
            self.test_results[0] += 1
        if self.test_archer.hitted == 2:
            self.test_results[1] += 1
        self.test_trials += 1
        self.test_archer.reset()
        self.test_archer.draw(canvas)
        self.evaluate_test_archer_shot(physics_consts.rain(), physics_consts.wind())

    def init_tests(self, best_player, gravity):
        self.best_player_ref = best_player
        self.gravity = gravity
        self.evaluate_test_archer_shot(physics_consts.rain(), physics_consts.wind())
