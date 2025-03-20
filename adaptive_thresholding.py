# BSD 3-Clause License

# Copyright (c) 2024, Pranjal Choudhury

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###################################################################################


import numpy as np
from scipy import ndimage


def custom_threshold(image, alpha=0.01):
    """
    Calculate the optimal threshold using custom entropy-based method.

    Parameters:
    - image (numpy.ndarray): Input image for threshold calculation.

    Returns:
    - optimal_threshold (int): Optimal threshold value for image segmentation.
    """
    hist = ndimage.histogram(image, min=0, max=np.max(
        image), bins=int(np.max(image)))  # Calculate histogram
    # Normalize histogram
    hist_norm = hist.ravel() / hist.sum()

    # Calculate entropies of foreground and background for all possible thresholds
    entropy_values = np.zeros(int(np.max(image)))
    for t in range(int(np.max(image))):
        p1 = hist_norm[:t+1].sum()
        p2 = hist_norm[t+1:].sum()

        entropy_values[t] = -p1 * \
            np.log(int(1/(1+p1))+p1) - p2 * np.log(int(1/(1+p2))+p2)

    # Find the optimal threshold based on mean entropy
    optimal_threshold = np.where(
        np.abs(entropy_values - np.mean(entropy_values)) < alpha)[0][-1]

    return optimal_threshold
