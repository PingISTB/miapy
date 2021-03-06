"""Enables the plotting of images for presentation and documentation purposes using the ``matplotlib`` library.

Refer also to `SimpleITK Notebooks
<http://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/10_matplotlib's_imshow.html>`_."""
import matplotlib.colors as plt_colors
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk


def plot_histogram(path: str, image: sitk.Image, no_bins: int=255, slice_no: int=-1,
                   title: str='', xlabel: str='', ylabel: str='') -> None:
    """Plots a histogram of an image.

    Plots either the histogram of a slice of the image or of the whole image.
    Args:
        path (str): The file path.
        image (SimpleITK.Image): The image.
        no_bins (int): The number of histogram bins.
        slice_no (int): The slice number or -1 to take the whole image.
        title (str): The histogram's title.
        xlabel (str): The histogram's x-axis label.
        ylabel (str): The histogram's y-axis label.

    Returns:
        None.
    """
    if slice_no > -1:
        data = sitk.GetArrayFromImage(image[:, :, slice_no])
    else:
        data = sitk.GetArrayFromImage(image)

    data = data.flatten()

    plt.hist(data, bins=no_bins)
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    plt.savefig(path)
    plt.close()


def plot_histogram_overlay(path: str, image1: sitk.Image, image2: sitk.Image, no_bins: int=255, slice_no: int=-1,
                           title: str='', xlabel: str='', ylabel: str='') -> None:
    """Plots a histogram of an image.

    Plots either the histogram of a slice of the image or of the whole image.
    Args:
        path (str): The file path.
        image1 (SimpleITK.Image): The first image.
        image2 (SimpleITK.Image): The second image.
        no_bins (int): The number of histogram bins.
        slice_no (int): The slice number or -1 to take the whole image.
        title (str): The histogram's title.
        xlabel (str): The histogram's x-axis label.
        ylabel (str): The histogram's y-axis label.

    Returns:
        None.
    """
    if slice_no > -1:
        data1 = sitk.GetArrayFromImage(image1[:, :, slice_no])
        data2 = sitk.GetArrayFromImage(image2[:, :, slice_no])
    else:
        data1 = sitk.GetArrayFromImage(image1)
        data2 = sitk.GetArrayFromImage(image2)

    data1 = data1.flatten()
    data2 = data2.flatten()

    plt.hist(data1, bins=no_bins, alpha=0.5)
    plt.hist(data2, bins=no_bins, alpha=0.5)
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    plt.savefig(path)
    plt.close()


def plot_slice(path: str, image: sitk.Image, slice_no: int) -> None:
    """Plots a slice from a 3-D image to a file.

    Args:
        path (str): The file path.
        image (SimpleITK.Image): The 3-D image.
        slice_no (int): The slice number.

    Returns:
        None
    """

    slice_ = sitk.GetArrayFromImage(image[:, :, slice_no])

    fig = plt.figure()
    # configure axes such that no boarder is plotted
    # refer to https://github.com/matplotlib/matplotlib/issues/7940/ about how to remove axis from plot
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.margins(0)
    ax.tick_params(which='both', direction='in')

    # plot image
    ax.imshow(slice_, 'gray', interpolation='none')

    fig.add_axes(ax)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(path, bbox_inches=extent)
    plt.close()


def plot_2d_segmentation(path: str, image, ground_truth, segmentation, alpha: float=0.5, label: int=1):
    """
    Plots a 2-dimensional image with an overlaid mask, which indicates under-, correct-, and over-segmentation.

    :param path: The save path.
    :type path: str
    :param image: The image.
    :type image: np.ndarray
    :param ground_truth: The ground truth.
    :type ground_truth: np.ndarray
    :param segmentation: The segmentation.
    :type segmentation: np.ndarray
    :param alpha: The alpha blending value, between 0 (transparent) and 1 (opaque).
    :type alpha: float
    :param label: The segmentation's label.
    :type label: int

    Example usage:

    >>> img = np.random.randn(10, 15) * 0.1
    >>> ground_truth = np.zeros((10, 15))
    >>> ground_truth[3:-3, 3:-3] = 1
    >>> segmentation = np.zeros((10, 15))
    >>> segmentation[4:-2, 4:-2] = 1
    >>> plotter.plot_2d_segmentation("/your/path/plot_2d_segmentation.png", img, ground_truth, segmentation)
    """

    if not image.shape == ground_truth.shape == segmentation.shape:
        raise ValueError("image, ground_truth, and segmentation must have equal shape")
    if not image.ndim == 2:
        raise ValueError("only 2-dimensional images supported")

    mask = np.zeros(ground_truth.shape)
    mask[np.bitwise_and(ground_truth == label, segmentation != label)] = 1  # under-segmentation
    mask[np.bitwise_and(ground_truth == label, segmentation == label)] = 2  # correct segmentation
    mask[np.bitwise_and(ground_truth != label, segmentation == label)] = 3  # over-segmentation
    masked = np.ma.masked_where(mask == 0, mask)

    fig = plt.figure()
    # configure axes such that no boarder is plotted
    # refer to https://github.com/matplotlib/matplotlib/issues/7940/ about how to remove axis from plot
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.margins(0)
    ax.tick_params(which='both', direction='in')

    # plot image and mask
    ax.imshow(image, 'gray', interpolation='none')
    cm = plt_colors.LinearSegmentedColormap.from_list('rgb',
                                                      [(1, 0, 0), (0, 1, 0), (0, 0, 1)], N=3)  # simple RGB color map
    ax.imshow(masked, interpolation='none', alpha=alpha, cmap=cm)

    fig.add_axes(ax)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(path, bbox_inches=extent)
    plt.close()
