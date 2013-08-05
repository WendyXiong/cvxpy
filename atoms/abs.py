from atom import Atom
import cvxpy.expressions.types as types
from cvxpy.expressions.variable import Variable
from cvxpy.expressions.curvature import Curvature
from cvxpy.expressions.shape import Shape
from cvxpy.constraints.affine import AffEqConstraint, AffLeqConstraint
from monotonicity import Monotonicity
import cvxpy.interface.matrix_utilities as intf

class abs(Atom):
    """ L1 norm sum(|x|) """
    def __init__(self, x):
        super(abs, self).__init__(x)

    # The shape is the same as the argument's shape.
    def set_shape(self):
        self._shape = Shape(*self.args[0].size)

    # Default curvature.
    def base_curvature(self):
        return Curvature.CONVEX

    def monotonicity(self):
        return [Monotonicity.NONMONOTONIC]

    # Any argument size is valid.
    def validate_arguments(self):
        pass

    @staticmethod
    def graph_implementation(var_args):
        x = var_args[0]
        rows,cols = x.size
        t = Variable(rows, cols)
        constraints = []
        for i in range(rows):
            for j in range(cols):
                constraints += [AffLeqConstraint(-t[i,j], x[i,j]), 
                                AffLeqConstraint(x[i,j], t[i,j])]
        return (t, constraints)

    # Return the absolute value of the argument at the given index.
    def index_object(self, key):
        x = self.args[0]
        return abs(x[key])