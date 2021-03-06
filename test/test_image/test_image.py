import unittest

import numpy as np
import SimpleITK as sitk

import miapy.image.image as img


class TestImageProperties(unittest.TestCase):
    def test_is_two_dimensional(self):
        x = 10
        y = 10
        image = sitk.Image([x, y], sitk.sitkUInt8)
        dut = img.ImageProperties(image)

        self.assertEqual(dut.is_two_dimensional(), True)
        self.assertEqual(dut.is_three_dimensional(), False)
        self.assertEqual(dut.is_vector_image(), False)

    def test_is_three_dimensional(self):
        x = 10
        y = 10
        z = 3
        image = sitk.Image([x, y, z], sitk.sitkUInt8)
        dut = img.ImageProperties(image)

        self.assertEqual(dut.is_two_dimensional(), False)
        self.assertEqual(dut.is_three_dimensional(), True)
        self.assertEqual(dut.is_vector_image(), False)

    def test_is_vector_image(self):
        x = 10
        y = 10
        number_of_components_per_pixel = 3
        image = sitk.Image([x, y], sitk.sitkVectorUInt8, number_of_components_per_pixel)
        dut = img.ImageProperties(image)

        self.assertEqual(dut.is_two_dimensional(), True)
        self.assertEqual(dut.is_three_dimensional(), False)
        self.assertEqual(dut.is_vector_image(), True)

    def test_properties(self):
        x = 10
        y = 10
        z = 3
        pixel_id = sitk.sitkUInt8
        size = (x, y, z)
        direction = (0, 1, 0, 1, 0, 0, 0, 0, 1)
        image = sitk.Image([x, y, z], pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut = img.ImageProperties(image)

        self.assertEqual(dut.size, size)
        self.assertEqual(dut.origin, size)
        self.assertEqual(dut.spacing, size)
        self.assertEqual(dut.direction, direction)
        self.assertEqual(dut.dimensions, z)
        self.assertEqual(dut.number_of_components_per_pixel, 1)
        self.assertEqual(dut.pixel_id, pixel_id)

    def test_equality(self):
        x = 10
        y = 10
        z = 3
        pixel_id = sitk.sitkUInt8
        size = (x, y, z)
        direction = (0, 1, 0, 1, 0, 0, 0, 0, 1)
        image = sitk.Image([x, y, z], pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut1 = img.ImageProperties(image)
        dut2 = img.ImageProperties(image)

        self.assertTrue(dut1 == dut2)
        self.assertFalse(dut1 != dut2)

        image = sitk.Image([x, y, z], sitk.sitkInt8)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut1 = img.ImageProperties(image)

        self.assertTrue(dut1 == dut2)
        self.assertFalse(dut1 != dut2)

        image = sitk.Image([x, y, z], sitk.sitkVectorUInt8, 2)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut1 = img.ImageProperties(image)

        self.assertTrue(dut1 == dut2)
        self.assertFalse(dut1 != dut2)

    def test_non_equality(self):
        x = 10
        y = 10
        z = 3
        pixel_id = sitk.sitkUInt8
        size = (x, y, z)
        direction = (0, 1, 0, 1, 0, 0, 0, 0, 1)
        image = sitk.Image([x, y, z], pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut1 = img.ImageProperties(image)

        different_size = (x, y, 2)

        # non-equal size
        image = sitk.Image(different_size, pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut2 = img.ImageProperties(image)

        self.assertFalse(dut1 == dut2)
        self.assertTrue(dut1 != dut2)

        # non-equal origin
        image = sitk.Image(size, pixel_id)
        image.SetOrigin(different_size)
        image.SetSpacing(size)
        image.SetDirection(direction)
        dut2 = img.ImageProperties(image)

        self.assertFalse(dut1 == dut2)
        self.assertTrue(dut1 != dut2)

        # non-equal spacing
        different_size = (x, y, 2)
        image = sitk.Image(size, pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(different_size)
        image.SetDirection(direction)
        dut2 = img.ImageProperties(image)

        self.assertFalse(dut1 == dut2)
        self.assertTrue(dut1 != dut2)

        # non-equal direction
        different_size = (x, y, 2)
        image = sitk.Image(size, pixel_id)
        image.SetOrigin(size)
        image.SetSpacing(size)
        image.SetDirection((1, 0, 0, 0, 1, 0, 0, 0, 1))
        dut2 = img.ImageProperties(image)

        self.assertFalse(dut1 == dut2)
        self.assertTrue(dut1 != dut2)


class TestSimpleITKNumpyImageBridge(unittest.TestCase):
    def test_convert(self):
        x = 10
        y = 10
        z = 3
        size = (x, y, z)
        image = sitk.Image([x, y, z], sitk.sitkUInt8)

        array, properties = img.SimpleITKNumpyImageBridge.convert(image)

        self.assertEqual(isinstance(array, np.ndarray), True)
        self.assertEqual(array.shape, (z, y, x))
        self.assertEqual(array.dtype, np.uint8)
        self.assertEqual(isinstance(properties, img.ImageProperties), True)
        self.assertEqual(properties.size, size)

    def test_convert_None(self):
        with self.assertRaises(ValueError):
            img.SimpleITKNumpyImageBridge.convert(None)
