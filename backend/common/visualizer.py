import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.ticker as mticker


def visualize(plot_type, data, state, date_from, date_to):
    """
    visualizes data by plot_type
    :param plot_type: type of graph e.g hist, pie_chart, line
    :param data: data in dict. form
    :return: image of the data
    """
    img = None
    plt.clf()
    if plot_type == "hist":
        plt.bar(list(data.keys()), data.values(), color='g')
        plt.xlabel("risk levels")
        plt.ylabel("number of days")
        plt.title("{}\nfrom {} to {}".format(state.upper(), date_from, date_to))

        fig = plt.gcf()
        img = _fig2img(fig)

    elif plot_type == "pie_chart":
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = list(data.keys())
        sizes = []
        for key in data.keys():
            sizes.append(data[key])
        explode = [0] * len(sizes)
        largest_i = 0
        explode[largest_i] = 0.1
        for i in range(len(sizes)):
            if sizes[i] > sizes[largest_i]:
                explode[largest_i] = 0
                largest_i = i
                explode[i] = 0.2
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("{}\nfrom {} to {}".format(state.upper(), date_from, date_to))

        fig = plt.gcf()
        img = _fig2img(fig)

    else:
        my_list = data.items()
        my_list = sorted(my_list)
        x, y = zip(*my_list)
        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
        plt.plot(x, y)
        plt.xticks(color='w')

        plt.xlabel("date")
        plt.ylabel("number of cases")
        plt.title("{}\nfrom {} to {}".format(state.upper(), date_from, date_to))
        fig = plt.gcf()
        img = _fig2img(fig)

    return img


def _fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


if __name__ == "__main__":
    img = visualize("line", {'2021-09-01': 1094249, '2021-09-02': 1096791, '2021-09-03': 1098526}, 'NY', '01-05-2021', '08-27-2021')
    img.show()