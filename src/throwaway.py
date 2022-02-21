from src.objects.individual import Population, Individual
from src.objects.chromosome import Chromosome, Codon
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

pop_size = 20
p_mutate = .01
p_cross = .8

def number_ones(chromosome):
    chrom = chromosome[0]
    chrom = chrom.codons[0].bitstring
    ans = 0
    for char in chrom:
        if char == "1":
            ans += 1
    return ans


def evolve():
    fig = plt.figure()
    ax = fig.add_subplot(111)  # create axis
    ax.axis('off')

    nums = np.random.choice(range(256), pop_size)
    pop = Population()
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        person.apply(number_ones)
        pop.add(person)

    im = plt.imshow(pop.to_array())

    def init():
        return [im]

    def animate(step):
        pop.evolve_one_step(p_cross, p_mutate, number_ones)
        im.set_array(pop.to_array())
        return [im]

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   init_func=init,
                                   frames=100,
                                   interval=50,
                                   blit=True)

    plt.show()


def main():
    import matplotlib
    matplotlib.use(
        'Qt5Agg')  # use Qt5 as backend, comment this line for default backend

    from matplotlib import pyplot as plt
    from matplotlib import animation

    fig = plt.figure()

    ax = plt.axes(xlim=(0, 2), ylim=(0, 100))

    N = 4
    lines = [plt.plot([], [])[0] for _ in range(N)]  # lines to animate

    rectangles = plt.bar([0.5, 1, 1.5], [50, 40, 90],
                         width=0.1)  # rectangles to animate

    patches = lines + list(rectangles)  # things to animate

    def init():
        # init lines
        for line in lines:
            line.set_data([], [])

        # init rectangles
        for rectangle in rectangles:
            rectangle.set_height(0)

        return patches  # return everything that must be updated

    def animate(i):
        # animate lines
        for j, line in enumerate(lines):
            line.set_data([0, 2], [10 * j, i])

        # animate rectangles
        for j, rectangle in enumerate(rectangles):
            rectangle.set_height(i / (j + 1))

        return patches  # return everything that must be updated

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=100, interval=20, blit=True)

    plt.show()


if __name__ == "__main__":
    evolve()

