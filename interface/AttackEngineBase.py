from typing import Callable, List, Tuple, Optional, Type
from gicaf.interface.ModelBase import ModelBase
from gicaf.interface.AttackBase import AttackBase
from gicaf.interface.LoggerBase import LoggerBase
import numpy as np
from abc import ABC, abstractmethod

class AttackEngineBase(ABC):

    @classmethod
    def version(cls): return "1.0"

    @abstractmethod
    def __init__(
        self, 
        data_generator: Callable[None, Tuple[np.ndarray, int]], 
        model: Type[ModelBase], 
        attacks: List[Type[AttackBase]],
        save: bool = True
    ) -> None: 
        """
        Initialize attack engine

        Parameters
        ----------
            data_generator : generator function
                Provides the samples loaded by the user
                Yields
                ------
                    x : numpy.ndarray
                        Image to use for attacks
                    y : int
                        Ground-truth of x 
            model : ModelBase
                Model to carry out attacks on
            attacks : list with elements of type AttackBase
                Attacks to carry out
        """
        ...

    @abstractmethod
    def run(
        self, 
        metric_names: Optional[List[str]] = None, 
        use_memory: bool = False
    ) -> Tuple[List[Type[LoggerBase]], List[float]]: 
        """
        Runs the attack

        Parameters
        ----------
            metric_names : list with elements of type string
                The metric names of the visual metrics to be collected. Default is
                None
            use_memory : bool
                Indicates whether or not to transfer knowledge from successful
                attacks to subsequent images of the same class. Memory is not to
                be transfered between different attack methods. Default is False
        Returns
        -------
            loggers : list with elements of type LoggerBase
                The experiment logs
            success_rates : list with elements of type float
                The experiment adversarial success rates in percentage
        Note
        ----
            This method must call 'self.model.reset_query_count()' before each attack to
            reset the model's query count
        """
        ...

    @abstractmethod
    def get_logs(self) -> List[Type[LoggerBase]]:
        """
        Get experiment logs

        Returns
        -------
            loggers : list with elements of type LoggerBase
                The experiment logs
        """
        ...

    @abstractmethod
    def close(self): 
        """
        End of session clean up
        """
        ...
