__author__ = 'purg'

import abc
import logging
import numpy

from smqtk.utils.plugin import ConfigurablePlugin


class DescriptorElement (ConfigurablePlugin):
    """
    Abstract descriptor vector container. The intent of this structure is to
    hide the specific method of storage of data (e.g. memory, file, database,
    etc.).

    This structure supports implementations that cache descriptor vectors on a
    per-UUID basis.

    Element implementations should be picklable for standard serialization.

    Descriptor element equality based on shared descriptor type and vector
    equality.

    """
    __metaclass__ = abc.ABCMeta

    # noinspection PyMethodOverriding
    @classmethod
    def from_config(cls, type_str, uuid, config_dict):
        """
        Instantiate a new instance of this class given the desired type, uuid,
        and JSON-compliant configuration dictionary.

        :param type_str: Type of descriptor. This is usually the name of the
            content descriptor that generated this vector.
        :type type_str: str

        :param uuid: Unique ID reference of the descriptor.
        :type uuid: collections.Hashable

        :param config_dict: JSON compliant dictionary encapsulating
            a configuration.
        :type config_dict: dict

        """
        return cls(type_str, uuid, **config_dict)

    def __init__(self, type_str, uuid):
        """
        Initialize a new descriptor element.

        :param type_str: Type of descriptor. This is usually the name of the
            content descriptor that generated this vector.
        :type type_str: str

        :param uuid: Unique ID reference of the descriptor.
        :type uuid: collections.Hashable

        """
        self._type_label = type_str
        self._uuid = uuid

    @property
    def _log(self):
        return logging.getLogger('.'.join([self.__module__,
                                           self.__class__.__name__]))

    def __hash__(self):
        return hash(self.uuid())

    def __eq__(self, other):
        if isinstance(other, DescriptorElement):
            b = self.vector() == other.vector()
            if isinstance(b, numpy.core.multiarray.ndarray):
                vec_equal = b.all()
            else:
                vec_equal = b
            return vec_equal and (self.type() == other.type())
        return False

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "%s{type: %s, uuid: %s}" % (self.__class__.__name__, self.type(),
                                           self.uuid())

    def uuid(self):
        """
        :return: Unique ID for this vector.
        :rtype: collections.Hashable
        """
        return self._uuid

    def type(self):
        """
        :return: Type label type of the ContentDescriptor that generated this
            vector.
        :rtype: str
        """
        return self._type_label

    ###
    # Abstract methods
    #

    @abc.abstractmethod
    def has_vector(self):
        """
        :return: Whether or not this container current has a descriptor vector
            stored.
        :rtype: bool
        """
        return

    @abc.abstractmethod
    def vector(self):
        """
        :return: Get the stored descriptor vector as a numpy array. This returns
            None of there is no vector stored in this container.
        :rtype: numpy.core.multiarray.ndarray or None
        """
        return

    @abc.abstractmethod
    def set_vector(self, new_vec):
        """
        Set the contained vector.

        If this container already stores a descriptor vector, this will
        overwrite it.

        :param new_vec: New vector to contain.
        :type new_vec: numpy.core.multiarray.ndarray

        """
        return
