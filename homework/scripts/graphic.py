from matplotlib import pyplot as plt

def plotter(x_arr, y_arr, x_rarr, y_rarr):

    # Locating the start point
    plt.axhline(color='black', lw=0.5)
    plt.axvline(color='black', lw=0.5) 
    
    ax1 = plt.subplot()
    ax2 = plt.subplot()

    ax1.plot(x_arr, y_arr, 'b', label="Real")
    ax2.plot(x_rarr, y_rarr, 'r', label ="Ideal")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.savefig('Fig.png')