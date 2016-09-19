#!/usr/bin/env python
# coding=utf-8

class Game:
    def __init__(self):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append(u"Pop问题 %s" % i)
            self.science_questions.append(u"Science问题 %s" % i)
            self.sports_questions.append(u"Sports问题 %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return u"Rock问题 %s" % index

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print player_name + u" 加入游戏"
        print u"一共有%s个玩家" % len(self.players)

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print u"轮到%s" % self.players[self.current_player]
        print u"他扔了%s点" % roll

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print u"%s 逃出了禁区" % self.players[self.current_player]
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12

                print self.players[self.current_player] + \
                            u'跑到了 ' + \
                            str(self.places[self.current_player])
                print u"目前的主题是 %s" % self._current_category
                self._ask_question()
            else:
                print u"%s 逃离禁区失败" % self.players[self.current_player]
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            print self.players[self.current_player] + \
                        u'跑到了 ' + \
                        str(self.places[self.current_player])
            print u"主题是 %s" % self._current_category
            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop': print self.pop_questions.pop(0)
        if self._current_category == 'Science': print self.science_questions.pop(0)
        if self._current_category == 'Sports': print self.sports_questions.pop(0)
        if self._current_category == 'Rock': print self.rock_questions.pop(0)

    @property
    def _current_category(self):
        if self.places[self.current_player] == 0: return 'Pop'
        if self.places[self.current_player] == 4: return 'Pop'
        if self.places[self.current_player] == 8: return 'Pop'
        if self.places[self.current_player] == 1: return 'Science'
        if self.places[self.current_player] == 5: return 'Science'
        if self.places[self.current_player] == 9: return 'Science'
        if self.places[self.current_player] == 2: return 'Sports'
        if self.places[self.current_player] == 6: return 'Sports'
        if self.places[self.current_player] == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print u'回答正确!!!!'
                self.purses[self.current_player] += 1
                print self.players[self.current_player] + \
                    u' 目前有 ' + \
                    str(self.purses[self.current_player]) + \
                    u' 个金币.'

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True



        else:

            print "回答正确!!!!"
            self.purses[self.current_player] += 1
            print self.players[self.current_player] + \
                u' 目前有 ' + \
                str(self.purses[self.current_player]) + \
                u' 个金币.'

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        print u'答案不正确'
        print self.players[self.current_player] + u" 被送往禁区"
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)


from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add(u'孙二娘')
    game.add(u'潘大壮')
    game.add(u'金三胖')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()
        if not not_a_winner: break
