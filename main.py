from ocular.app import DevApp


def main():
    DevApp().run()

    # plt.rcParams['figure.figsize'] = [12,9]
    # fig, ax = plt.subplots()
    # apparent_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    # true_angle_of_view_viz.make_plot(ax, telescope, eyepieces)
    # true_field_of_view_viz.make_plot(ax, telescope, eyepieces)
    # field_stop_diameter_viz.make_plot(ax, telescope, eyepieces)
    # ax.legend()
    # plt.draw() # Way to draw multple plots in different windows.
    # plt.show() # Only do this once.


if __name__ == '__main__':
    main()
