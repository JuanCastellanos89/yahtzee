import random
import matplotlib.pyplot as plt

class Dice:
    def __init__(self):
        self.value = 0
        self.locked = False
    
    def roll(self):
        if not self.locked:
            self.value = random.randint(1, 6)
    
    def __str__(self):
        return str(self.value)

class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = {
            "Ones": None,
            "Twos": None,
            "Threes": None,
            "Fours": None,
            "Fives": None,
            "Sixes": None,
            "Three of a kind": None,
            "Four of a kind": None,
            "Full House": None,
            "Small Straight": None,
            "Large Straight": None,
            "Yahtzee": None,
            "Chance": None
        }
        self.total_score = 0
        self.category_counts = {
            "Ones": 0,
            "Twos": 0,
            "Threes": 0,
            "Fours": 0,
            "Fives": 0,
            "Sixes": 0,
            "Three of a kind": 0,
            "Four of a kind": 0,
            "Full House": 0,
            "Small Straight": 0,
            "Large Straight": 0,
            "Yahtzee": 0,
            "Chance": 0
        }
    
    def calculate_score(self, category, dice):
        if category == "Ones":
            return sum(d for d in dice if d == 1)
        elif category == "Twos":
            return sum(d for d in dice if d == 2)
        elif category == "Threes":
            return sum(d for d in dice if d == 3)
        elif category == "Fours":
            return sum(d for d in dice if d == 4)
        elif category == "Fives":
            return sum(d for d in dice if d == 5)
        elif category == "Sixes":
            return sum(d for d in dice if d == 6)
        elif category == "Three of a kind":
            if any(dice.count(d) >= 3 for d in dice):
                return sum(dice)
            else:
                return 0
        elif category == "Four of a kind":
            if any(dice.count(d) >= 4 for d in dice):
                return sum(dice)
            else:
                return 0
        elif category == "Full House":
            counts = [dice.count(d) for d in set(dice)]
            if 2 in counts and 3 in counts:
                return 25
            else:
                return 0
        elif category == "Small Straight":
            if any(
                (1 in dice and 2 in dice and 3 in dice and 4 in dice) or
                (2 in dice and 3 in dice and 4 in dice and 5 in dice) or
                (3 in dice and 4 in dice and 5 in dice and 6 in dice)
                for _ in range(2)
            ):
                return 30
            else:
                return 0
        elif category == "Large Straight":
            if any(
                (1 in dice and 2 in dice and 3 in dice and 4 in dice and 5 in dice) or
                (2 in dice and 3 in dice and 4 in dice and 5 in dice and 6 in dice)
                for _ in range(2)
            ):
                return 40
            else:
                return 0
        elif category == "Yahtzee":
            if len(set(dice)) == 1:
                return 50
            else:
                return 0
        elif category == "Chance":
            return sum(dice)
        
        return 0  # Manejo por defecto si la categoría no es reconocida o el puntaje es None

    def decide_keepers(self, dice, scorecard):
        # Implementación de una estrategia más sofisticada para decidir qué dados mantener
        keepers = []
        
        # Ordena los dados de mayor a menor valor
        dice.sort(reverse=True)
        
        # Verifica si ya hay una combinación completa (yahtzee, full house, straight, etc.)
        if self.is_full_house(dice) and scorecard["Full House"] is None:
            keepers = dice[:]
        elif self.is_large_straight(dice) and scorecard["Large Straight"] is None:
            keepers = dice[:]
        elif self.is_small_straight(dice) and scorecard["Small Straight"] is None:
            keepers = dice[:]
        elif self.is_yahtzee(dice) and scorecard["Yahtzee"] is None:
            keepers = dice[:]
        elif self.is_four_of_a_kind(dice) and scorecard["Four of a kind"] is None:
            keepers = dice[:]
        elif self.is_three_of_a_kind(dice) and scorecard["Three of a kind"] is None:
            keepers = dice[:]
        else:
            # Si ninguna combinación especial está disponible, conserva los dados más altos
            keepers = dice[:]

        return keepers
    
    def is_full_house(self, dice):
        counts = [dice.count(d) for d in set(dice)]
        return 2 in counts and 3 in counts
    
    def is_large_straight(self, dice):
        return (1 in dice and 2 in dice and 3 in dice and 4 in dice and 5 in dice) or \
               (2 in dice and 3 in dice and 4 in dice and 5 in dice and 6 in dice)
    
    def is_small_straight(self, dice):
        return (1 in dice and 2 in dice and 3 in dice and 4 in dice) or \
               (2 in dice and 3 in dice and 4 in dice and 5 in dice) or \
               (3 in dice and 4 in dice and 5 in dice and 6 in dice)
    
    def is_yahtzee(self, dice):
        return len(set(dice)) == 1
    
    def is_four_of_a_kind(self, dice):
        return any(dice.count(d) >= 4 for d in dice)
    
    def is_three_of_a_kind(self, dice):
        return any(dice.count(d) >= 3 for d in dice)

    def play_turn(self):
        dice = [Dice() for _ in range(5)]
        
        # Realizar tres lanzamientos
        for roll_num in range(1, 4):
            for die in dice:
                die.roll()
            
            if roll_num < 3:
                # Decidir qué dados mantener
                keepers = self.decide_keepers([die.value for die in dice], self.scorecard)
                
                # Bloquear los dados seleccionados
                for i, die in enumerate(dice):
                    if die.value not in keepers:
                        die.locked = False
                    else:
                        die.locked = True
                        
                    # Volver a lanzar dados no bloqueados
                    if not die.locked:
                        die.roll()

        dice_values = [die.value for die in dice]

        # Elegir la mejor categoría disponible para maximizar el puntaje
        available_categories = [cat for cat, score in self.scorecard.items() if score is None]
        best_category = self.select_best_category(available_categories, dice_values, self.scorecard)
        max_score = self.calculate_score(best_category, dice_values)

        # Registrar el puntaje en la tarjeta de puntuación y sumarlo al total
        self.scorecard[best_category] = max_score
        self.total_score += max_score

        # Contar la frecuencia de obtención de cada categoría
        if best_category in self.category_counts:
            self.category_counts[best_category] += 1

    def select_best_category(self, available_categories, dice_values, scorecard):
        max_score = 0
        best_category = None
        
        for category in available_categories:
            score = self.calculate_score(category, dice_values)
            
            # Prioriza las categorías que aún no tienen puntaje
            if scorecard[category] is None:
                if score > max_score:
                    max_score = score
                    best_category = category
            else:
                # Si la categoría ya tiene puntaje, evalúa si cambiar a otra categoría
                current_score = scorecard[category]
                if score > current_score:
                    max_score = score
                    best_category = category
        
        return best_category

    def get_total_score(self):
        return self.total_score

def simulate_games(num_games):
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    player1_scores = []
    player2_scores = []

    for _ in range(num_games):
        for _ in range(13):  # 13 turnos por juego
            player1.play_turn()
            player2.play_turn()

        # Guardar puntajes totales al final de cada juego
        player1_scores.append(player1.get_total_score())
        player2_scores.append(player2.get_total_score())

        # Reiniciar la puntuación total para la siguiente partida
        player1.total_score = 0
        player2.total_score = 0
       
        player1.scorecard = {cat: None for cat in player1.scorecard}
        player2.scorecard = {cat: None for cat in player2.scorecard}

    print(f"\nSimulación completa de {num_games} juegos.")
    print(f"Puntaje total después de {num_games} juegos:")
    print(f"{player1.name}: {sum(player1_scores)} puntos")
    print(f"{player2.name}: {sum(player2_scores)} puntos")

    # Generar histogramas de los puntajes totales
    plt.figure(figsize=(12, 6))
    plt.hist(player1_scores, bins=20, alpha=0.7, label=player1.name, color='blue', edgecolor='black')
    plt.hist(player2_scores, bins=20, alpha=0.7, label=player2.name, color='orange', edgecolor='black')
    plt.axvline(sum(player1_scores)/len(player1_scores), color='blue', linestyle='dashed', linewidth=1)
    plt.axvline(sum(player2_scores)/len(player2_scores), color='orange', linestyle='dashed', linewidth=1)
    plt.text(sum(player1_scores)/len(player1_scores)*0.9, plt.ylim()[1]*0.9, f'Mean: {sum(player1_scores)/len(player1_scores):.2f}', color = 'blue')
    plt.text(sum(player2_scores)/len(player2_scores)*1.1, plt.ylim()[1]*0.9, f'Mean: {sum(player2_scores)/len(player2_scores):.2f}', color = 'orange')
    plt.xlabel('Puntaje total')
    plt.ylabel('Frecuencia')
    plt.title(f'Distribución de puntajes totales después de {num_games} juegos')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Generar histogramas de categorías específicas
    categories = list(player1.category_counts.keys())
    for category in categories:
        plt.figure(figsize=(12, 6))
        x = [player1.name, player2.name]
        y = [player1.category_counts[category], player2.category_counts[category]]

        plt.bar(x, y, color=['blue', 'orange'])
        plt.ylabel('Frecuencia')
        plt.title(f'Frecuencia de obtención de la categoría "{category}" después de {num_games} juegos')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    simulate_games(10000)
