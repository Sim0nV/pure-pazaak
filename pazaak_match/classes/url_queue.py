from constants import env


class URLQueue:
    """URL String Queue"""

    PRIORITY_SOUNDS = [
        env.MATCH_END_SOUND,
        env.ROUND_END_SOUND,
        env.FORFEIT_TIMEOUT_SOUND,
    ]  # Priority sounds to avoid skipping

    def __init__(self, size: int):
        """Initialize string queue of passed size

        Args:
            size (int): Size of queue to initialize
        """
        self.size = size
        self.queue = [""] * size

    def clear_half_of_queue(self):
        """Clears half of URL queue if priority sound not present"""
        if not any(
            x in self.queue[self.size // 2 : self.size - 1]  # noqa: E203
            for x in self.PRIORITY_SOUNDS
        ):
            # If priority sound not found in back half of queue,
            # Clear back half of queue
            for index in range(self.size // 2, self.size - 1):
                self.queue[index] = ""
        else:
            if env.IS_DEBUG_MODE:
                print(
                    "Skipping clear since priority sound present in: ",
                    self.queue,
                )

    def enqueue(self, url: str):
        """Enqueue passed URL string to URL queue,

        Args:
            url (str): _description_
        """
        if self.queue[self.size - 1] != "":
            # If queue full:
            if env.IS_DEBUG_MODE:
                print("Clearing half of: ", self.queue)
            self.clear_half_of_queue()  # Clear half of queue
            self.queue[self.size // 2] = url  # Enqueue new element
            if env.IS_DEBUG_MODE:
                print("Half cleared, now: ", self.queue)
        else:
            self.queue[self.queue.index("")] = url
            if env.IS_DEBUG_MODE:
                print("Queued, now: ", self.queue)

    def pop(self) -> str:
        """Removes and returns first URL in URL queue

        Returns:
            str: First URL in queue
        """

        url = self.queue.pop(0)
        if len(self.queue) < self.size:
            # If queue size less than passed size,
            # Append empty string so size matches
            self.queue.append("")
        if env.IS_DEBUG_MODE:
            print("Popped, now: ", self.queue)
        return url

    def is_empty(self) -> bool:
        """Returns true if queue is empty, false otherwise

        Returns:
            bool: True if queue is empty, false otherwise
        """
        return self.queue[0] == ""
