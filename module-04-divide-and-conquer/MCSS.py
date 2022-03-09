import sys

# Function to find the maximum sublist sum using divide-and-conquer
def MCSS(nums, left=None, right=None):

	# base case
	if not nums:
		return 0

	if left is None and right is None:
		left, right = 0, len(nums) - 1

	# If the list contains 0 or 1 element
	if right == left:
		return nums[left]

	# Find the middle element in the list
	mid = (left + right) // 2


	# Recursively find the maximum sublist sum for the left
	# and right sublist, and take maximum
	maxL = MCSS(nums, left, mid)
	maxR = MCSS(nums, mid + 1, right)


	# Find maximum sublist sum for the left sublist,
	# including the middle element
	leftMax = -sys.maxsize
	total = 0
	for i in range(mid, left - 1, -1):
		total += nums[i]
		if total > leftMax:
			leftMax = total

	# Find maximum sublist sum for the right sublist,
	# excluding the middle element
	rightMax = -sys.maxsize
	total = 0		# reset sum to 0

	for i in range(mid + 1, right + 1):
		total += nums[i]
		if total > rightMax:
			rightMax = total

	maxM = leftMax + rightMax

	# return the maximum of the three
	return max(maxL, maxM, maxR)


if __name__ == '__main__':

	nums = [1, -2, 0, 3, -1, 0, 2, -3]
	print('The Maximum sum of the sublist is', MCSS(nums))
