# Copyright (C) 2011, 2012 Ben Elliston
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

"""Transmission model details."""
import numpy as np
import polygons
from costs import annuity_factor


class Transmission:

    """An encapsulating class for transmission specific bits."""

    def __init__(self, costfn, discount, lifetime=50):
        """Construct transmission costs given a cost function, discount rate and lifetime.

        >>> t = Transmission(30, 0.05)
        """
        # Vectorise the cost function so that we can call it with a matrix argument.
        self.costfn = np.vectorize(costfn)
        self.af = annuity_factor(lifetime, discount)
        self.dist_matrix = polygons.distances

    def cost_matrix(self, capacities):
        """Return the cost matrix given a lambda function and capacity matrix.

        >>> t = Transmission(lambda x: x / 10, 30, 0.05)
        >>> caps = np.empty(polygons.distances.shape)
        >>> caps.fill(100)
        >>> costmat = t.cost_matrix(caps)
        >>> costmat[1:, 1:].min()
        0.0
        >>> costmat[1:, 1:].max().round()
        553345356.0
        """
        cost_per_mw_km = self.costfn(capacities)
        return cost_per_mw_km * capacities * self.dist_matrix / self.af
