# general
chars = ("o", "h", "a", "i", "s", "e", "p", "t", "u", "c", "q", "g", "n", "4", "7")
words = ("push", "nice", "enough", "change", "question", "teaching")
passwords = (
    "p7go", "up4i", "shu7", "qaq4",
    "ieth4", "aogh4", "gae7o", "oon7i",
    "niequai4", "toaghu7i", "aetoh4co", "uing7tha", "ohcei4ha", "cie4quoo"
)
shift_passwords = (
    "Es4Q", "7oSe", "4iNu", "nUs7",
    "Cha4a", "ieSh4", "Oone4", "gaeT4",
    "thoi4Toh", "ieChaes4", "oiNg4coo", "Goingai4", "teicha4E", "HooNgu4e"
)
random_passwords = (
    "s4ci", "ecia", "tg7n", "u74o",
    "7one4", "q4itn", "ucthg", "neeg7",
    "aeap74an", "eggos7hu", "ps4gaq7u", "onect4ae", "7nghptsp", "aqchch4e"
)
random_shift_passwords = (
    "S4cE", "teN7", "7tiT", "eQ74",
    "ctS4e", "hH4uS", "ieT4U", "ThC7g",
    "7hGenToI", "oNe4gAnG", "G7HpnhNo", "teTgH4Ts", "gTiCgs7T", "UoPtOiE7"
)
key_pairs = [('p', 'u'), ('u', 's'), ('s', 'h'), ('n', 'i'), ('i', 'c'), ('c', 'e'), ('e', 'n'), ('n', 'o'), ('o', 'u'), ('u', 'g'), ('g', 'h'), ('c', 'h'), ('h', 'a'), ('a', 'n'), ('n', 'g'), ('g', 'e'), ('q', 'u'), ('u', 'e'), ('e', 's'), ('s', 't'), ('t', 'i'), ('i', 'o'), ('o', 'n'), ('t', 'e'), ('e', 'a'), ('a', 'c'), ('h', 'i'), ('i', 'n'), ('i', 'e'), ('e', 'q'), ('u', 'a'), ('a', 'i'), ('i', '4'), ('t', 'o'), ('o', 'a'), ('a', 'g'), ('h', 'u'), ('u', '7'), ('7', 'i'), ('a', 'e'), ('e', 't'), ('o', 'h'), ('h', '4'), ('4', 'c'), ('c', 'o'), ('u', 'i'), ('g', '7'), ('7', 't'), ('t', 'h'), ('h', 'c'), ('e', 'i'), ('4', 'h'), ('c', 'i'), ('e', '4'), ('4', 'q'), ('u', 'o'), ('o', 'o'), ('a', 'p'), ('p', '7'), ('7', '4'), ('4', 'a'), ('e', 'g'), ('g', 'g'), ('g', 'o'), ('o', 's'), ('s', '7'), ('7', 'h'), ('p', 's'), ('s', '4'), ('4', 'g'), ('g', 'a'), ('a', 'q'), ('q', '7'), ('7', 'u'), ('n', 'e'), ('e', 'c'), ('c', 't'), ('t', '4'), ('7', 'n'), ('h', 'p'), ('p', 't'), ('t', 's'), ('s', 'p'), ('q', 'c'), ('4', 'e'), ('n', 'h'), ('p', 'i'), ('c', 'g'), ('c', '7'), ('n', 't'), ('4', 'i'), ('q', 'n'), ('4', 't'), ('p', 'a'), ('p', 'q'), ('g', '4'), ('i', 't'), ('n', '7'), ('g', 'i'), ('7', 'g'), ('h', 'n'), ('7', 'o'), ('p', 'n'), ('h', 'h'), ('u', 'c'), ('g', 'p'), ('e', '7'), ('p', '4'), ('n', 'u'), ('g', 's'), ('p', 'o'), ('q', 'a'), ('a', 'o'), ('t', 'n'), ('s', 'i'), ('a', '4'), ('4', 'u'), ('e', 'e'), ('g', 'u'), ('q', 's'), ('i', 'p'), ('q', '4'), ('c', 'n'), ('o', 'g'), ('o', '4'), ('g', 't'), ('h', 'g'), ('s', 'n'), ('t', 'q'), ('c', 'q'), ('o', 'i'), ('q', 'p'), ('i', 'h'), ('i', 'a'), ('u', 'p'), ('t', 'g'), ('o', 'p'), ('u', '4'), ('n', 'n'), ('n', 'p'), ('s', 'e'), ('h', 'o')]

shift = "(shift)"

# key_pair_generator.py
random_seed = 1337

# path/folders and so on
users_file_name = "raw_data/users"
completed_tasks_file_name = "completed_tasks"
task_completed = "all"
transitions_file_name = "transitions"
observations_file_name = "observations"
