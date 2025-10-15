from abc import ABC, abstractmethod

class AbstractUserRegistrationService(ABC):

    @abstractmethod
    def register_user(self, cleaned_data, user_type):
        pass
