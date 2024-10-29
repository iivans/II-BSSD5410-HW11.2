import random, sys, math

def makerule_char(data, context):
    '''Make a rule dict for given data based on character sequences.'''
    rule = {}
    index = context
    
    for i in range(index, len(data)):
        key = data[i - context:i]
        next_char = data[i]
        if key in rule:
            rule[key].append(next_char)
        else:
            rule[key] = [next_char]

    return rule

def makestring_with_temp(rule, length, temperature=1.0):
    '''Generate string with temperature control for randomness.'''
    oldchars = random.choice(list(rule.keys()))  # random starting sequence
    string = oldchars
    
    for _ in range(length):
        try:
            key = oldchars
            options = rule[key]
            
            # Adjust randomness using temperature
            if temperature < 1.0:
                counts = {char: options.count(char) for char in set(options)}
                total = sum([count ** (1.0 / temperature) for count in counts.values()])
                adjusted_probs = {char: (count ** (1.0 / temperature)) / total for char, count in counts.items()}
                newchar = random.choices(list(adjusted_probs.keys()), list(adjusted_probs.values()))[0]
            else:
                newchar = random.choice(options)
                
            string += newchar
            oldchars = oldchars[1:] + newchar

        except KeyError:
            return string
    return string

if __name__ == '__main__':
    # Input parameters from the user
    num_files = int(input("How many text files do you want to combine? "))
    files = [input(f"Enter file name {i+1}: ") + ".txt" for i in range(num_files)]  # Automatically append .txt
    context_size = int(input("Enter the context size (window size): "))
    gen_length = int(input("Enter the length of text to generate: "))
    temperature = float(input("Enter the randomness temperature (0-1, 1 for max randomness): "))

    # Read and combine all text files
    combined_data = ""
    for file in files:
        with open(file, encoding='utf8') as f:
            combined_data += f.read() + " "

    # Create rule based on characters
    rule = makerule_char(combined_data, context_size)

    # Generate text with temperature control
    generated_text = makestring_with_temp(rule, gen_length, temperature)
    print(generated_text)
