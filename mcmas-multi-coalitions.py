import sys
import os
import datetime
import itertools

def main(args):
    MCMAS_PATH = args[1]
    MCMAS_PARAMS = args[2].replace('"', '')
    ISPL_FILE = args[3]

    agents = get_agents(ISPL_FILE)
    # print('Agents:', agents)
    requirements = get_requirements(ISPL_FILE, len(agents))
    # print('Requirements:', requirements)
    coalitions = generate_coalitions(requirements, agents)
    start = datetime.datetime.now()
    good_coalitions = mcmas(MCMAS_PATH, MCMAS_PARAMS, ISPL_FILE, coalitions)
    end = datetime.datetime.now()
    print('Good coalitions:')
    for good_coalition in good_coalitions:
        print(good_coalition)
    print('### Execution time:', (end-start).microseconds / 1000, '[ms]')




def mcmas(MCMAS_PATH, MCMAS_PARAMS, ispl, coalitions):
    good_coalitions = []
    n = len(coalitions.keys())
    permutation = []
    link = []
    n_permutations = 1
    for var in coalitions:
        permutation.append(0)
        link.append(var)
        n_permutations = n_permutations * len(coalitions[var])
    for j in range(0, n_permutations):
        coalition = {}
        for i in range(0, n):
            coalition[link[i]] = coalitions[link[i]][permutation[i]]
        add_coalitions(ispl, coalition)
        stream = os.popen(MCMAS_PATH + 'mcmas ' + MCMAS_PARAMS + './tmp.ispl')
        output = stream.read()
        if is_satisfied(output):
            good_coalitions.append(coalition)
        for i in range(0, n):
            permutation[i] = (permutation[i] + 1) % len(coalitions[link[i]])
            if permutation[i] != 0:
                break
    return good_coalitions

def add_coalitions(ispl, coalition):
    with open(ispl) as file:
        content = file.read()
    i = content.find('Groups')
    j = content.find('end Groups')
    new_groups = 'Groups\n'
    for var in coalition:
        new_groups = new_groups + var + ' = {' + ','.join(coalition[var]) + '};\n'
    new_groups = new_groups + 'end Groups\n'
    content = content[:i] + new_groups + content[j+10:]
    with open('tmp.ispl', 'w') as file:
        file.write(content)

def generate_coalitions(requirements, agents):
    coalitions = {}
    for (var, min, max, together, split) in requirements:
        c = []
        for size in range(min, max+1):
            coalitions_size = list(itertools.combinations(agents, size))
            for coalition in coalitions_size:
                skip = False
                for ts in together:
                    s = sum([ag in coalition for ag in ts])
                    if s != 0 and s != len(ts):
                        skip = True
                        break
                if skip: continue
                for sp in split:
                    if sum([ag in coalition for ag in sp]) >= 2:
                        skip = True
                        break
                if skip: continue
                c.append(coalition)
        coalitions[var] = c
    return coalitions

def get_requirements(ispl, n):
    requirements = []
    with open(ispl) as file:
        content = file.read()
    i = content.find('Groups')
    j = content.find('end Groups')
    content = content[i+6:j]
    while '{' in content and '}' in content:
        j = content.find('=')
        g = content[:j].strip()
        i = content.find('min:')
        j = content.find(';', i)
        k = content.find('}', i)
        j = min(j, k)
        if i == -1:
            min_c = 0
        else:
            min_c = content[i+4:j].strip()
        i = content.find('max:')
        j = content.find(';', i)
        k = content.find('}', i)
        j = min(j, k)
        if i == -1:
            max_c = n
        else:
            max_c = content[i+4:j].strip()
        i = content.find('together:')
        j = content.find(';', i)
        k = content.find('}', i)
        j = min(j, k)
        together = []
        if i != -1:
            for ts in content[i+9:j].split(','):
                s = set()
                for ts1 in ts.split('~'):
                    s.add(ts1.strip())
                together.append(s)
        i = content.find('split:')
        j = content.find(';', i)
        k = content.find('}', i)
        j = min(j, k)
        split = []
        if i != -1:
            for ts in content[i+6:j].split(','):
                s = set()
                for ts1 in ts.split('~'):
                    s.add(ts1.strip())
                split.append(s)
        requirements.append((g, int(min_c), int(max_c), together, split))
        content = content[content.find('}')+1:]
    return requirements

def get_agents(ispl):
    agents = []
    with open(ispl) as file:
        content = file.read()
    while 'Agent ' in content:
        i = content.find('Agent ')
        j = content.find(' ', i+6)
        k = content.find('\n', i+6)
        j = min(j, k)
        agent = content[i+6:j]
        agents.append(agent)
        content = content[j:]
    return agents

def is_satisfied(mcmas_res):
    if 'FALSE in the model' in mcmas_res:
        return False
    else:
        return True

if __name__ == '__main__':
    main(sys.argv)
