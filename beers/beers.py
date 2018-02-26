def count_beers(money,cap,bottles,drinked_beers):
    new_beers=money//2+cap//4+bottles//2
    rest_money=money%2
    rest_cap=cap%4+new_beers
    rest_bottles=bottles%2+new_beers
    rest_money=rest_money
    drinked_beers=drinked_beers+new_beers
    print(rest_money,rest_cap,rest_bottles,drinked_beers)
    if rest_money<2 and rest_cap<4 and rest_bottles<2:
        print('Game Over!')
        return drinked_beers
    else:
        return count_beers(rest_money,rest_cap,rest_bottles,drinked_beers)

if __name__=='__main__':
    beers=count_beers(10,0,0,0)
    print(beers)
