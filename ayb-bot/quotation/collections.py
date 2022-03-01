from .quote_factory import QuoteFactory

FACTS = [
    "Dental floss has superb tensile strength.",
    "The square root of rope is string.",
    "Humans can survive underwater. But not for very long.",
    "According to most advanced algorithms, the world's best name is Craig.",
    "This situation is hopeless.",
    "Tungsten has the highest melting point of any metal.",
    "Before the invention of scrambled eggs in 1912, the typical breakfast ",
    "was either whole eggs still in the shell or scrambled rocks.",
    "In Greek myth, the craftsman Daedalus invented human flight so a group ",
    "of Minotaurs would stop teasing him about it.",
]

MEMES = [
    "Somebody set up us the bomb.",
    "Main screen turn on.",
    "All your base are belong to us.",
    "You have no chance to survive make your time.",
    "Move ZIG for great justice."
]


class FactQuotes(QuoteFactory):
    def __init__(self):
        super().__init__(FACTS)


class MemeQuotes(QuoteFactory):
    def __init__(self):
        super().__init__(MEMES)
