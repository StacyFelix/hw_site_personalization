from django.shortcuts import render

from .models import Player, Game, PlayerGameInfo
from .forms import GameForm
from django import http


def show_home(request):
    # request.session.clear()
    # если в сессии нет id_player, то:
    if not request.session.get('id_player'):
        # создается в таблице Player запись
        player = Player.objects.create()
        id_player = player.id
        # в сессию записывается id_player
        request.session['id_player'] = id_player
    else:
        id_player = request.session['id_player']
        player = Player.objects.get(id=id_player)
    # print(id_player)
    # print(player)

    form = GameForm()
    res = ''

    if not request.session.get('amount'):
        request.session['amount'] = 0
    if not request.session.get('creator'):
        request.session['creator'] = False

    game_last = Game.objects.last()
    if game_last is None:
        flag = False
    else:
        if not game_last.status:
            flag = False
        else:
            flag = True

    # если статус последней игры != True (False окончена) или вообще нет игр
    if not flag:
        game_begin = False

        if request.method == 'POST':
            data_form = GameForm(request.POST)
            if data_form.is_valid():
                # создать в таблице Game запись: id_game, статус = True(начата), загаданное число
                game = Game.objects.create(number=data_form.data['number'], status=True)
                id_game = game.id
                # создать в таблице PlayerGameInfo запись: id_game, id_player, флаг создатель = 1
                PlayerGameInfo.objects.create(creator=True, player=player, game=game)
                # в сессию записывается id_game
                request.session['id_game'] = id_game
                return http.HttpResponseRedirect('')
    else:
        game_begin = True
        game_last = Game.objects.last()
        id_game = game_last.id
        # найти запись по id_player и id_game, вытащить из БД флаг создателя
        try:
            player_game_info = PlayerGameInfo.objects.get(player__id=id_player, game__id=id_game)
        except PlayerGameInfo.DoesNotExist:
            player_game_info = None
        # если нашелся, то:
        if player_game_info is not None:
            # если флаг создателя = 1, то:
            if player_game_info.creator:
                request.session['creator'] = True
            else:
                if request.method == 'POST':
                    data_form = GameForm(request.POST)
                    if data_form.is_valid():
                        if not request.session.get('amount'):
                            request.session['amount'] = 0
                        request.session['amount'] += 1
                        game_last.amount = game_last.amount + 1
                        game_last.save()
                        if game_last.number == int(data_form.data['number']):
                            game_last.status = False
                            game_last.save()
                            return http.HttpResponseRedirect('')
                        else:
                            if game_last.number > int(data_form.data['number']):
                                res = f"Число > {data_form.data['number']}"
                            else:
                                res = f"Число < {data_form.data['number']}"
        else:
            request.session['creator'] = False
            # создать в таблице PlayerGameInfo запись: id_game, id_player, флаг создатель = 0
            PlayerGameInfo.objects.create(creator=False, player=player, game=game_last)
            # в сессию записывается id_game
            request.session['id_game'] = id_game
            request.session['amount'] = 0

    context = {
        'form': form,
        'game_begin': game_begin,
        'creator': request.session['creator'],
        'game': game_last,
        'res': res,
        'amount': request.session['amount'] # количество попыток для конкретного игрока
    }
    template = 'home.html'
    # context ={}

    return render(request, template, context)
