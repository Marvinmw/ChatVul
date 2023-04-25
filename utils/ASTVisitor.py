#  Copyright [2022] [MA WEI @ NTU], ma_wei@ntu.edu.sg

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#load parsers
"""
This module implements the visitor design pattern for Tree-sitter.
https://github.com/tree-sitter/py-tree-sitter/blob/4e2e765c5d8cf946b886bc757aef5cbf907c82b8/tests/test_tree_sitter.py
"""

class ASTVisitor:
    """
    Visitor to traverse a given abstract syntax tree

    The class implements the visitor design pattern
    to visit nodes inside an abstract syntax tree.
    The syntax tree is traversed in pre-order by employing
    a tree cursor.

    Custom visitors should subclass the ASTVisitor:

    ```
    class AllNodesVisitor(tree_sitter.ASTVisitor):

        def visit_module(self, module_node):
            # Called for nodes of type module only
            ...

        def visit(self, node):
            # Called for all nodes where a specific handler does not exist
            # e.g. here called for all nodes that are not modules
            ...

        def visit_string(self, node):
            # Stops traversing subtrees rooted at a string
            # Traversal can be stopped by returning False
            return False

    ```
    """

    def visit(self, node):
        """Default handler that captures all nodes not already handled"""
        return True

    def visit_ERROR(self, error_node):
        """
        Handler for errors marked in AST.

        The subtree below an ERROR node can sometimes form unexpected AST structures.
        The default strategy is therefore to skip all subtrees rooted at an ERROR node.
        Override for a custom error handler.
        """
        return False

    # Traversing ----------------------------------------------------------------

    def on_visit(self, node):
        """
        Handles all nodes visted in AST and calls the underlying vistor methods.

        This method is called for all discovered AST nodes first.
        Override this to handle all nodes regardless of the defined visitor methods.

        Returning False stops the traversal of the subtree rooted at the given node.
        """
        visitor_fn = getattr(self, f"visit_{node.type}", self.visit)
        if len(node.children) == 0:
            return False
        return visitor_fn(node)

    def walk(self, tree):
        """
        Walks a given (sub)tree by using the cursor API

        This method walks every node in a given subtree in pre-order traversal.
        During the traversal, the respective visitor method is called.
        """

        cursor   = tree.walk()
        has_next = True

        while has_next:
            current_node = cursor.node

            if self.on_visit(current_node):
                has_next = cursor.goto_first_child()
            else:
                has_next = False

            if not has_next:
                has_next = cursor.goto_next_sibling()

            while not has_next and cursor.goto_parent():
                has_next = cursor.goto_next_sibling()
    
    def _getAllSubNodes(self, node):
        nodes = [node]
        if len(node.children) == 0:
            return [node]
        else:
            for n in node.children:
                nodes += self._getAllSubNodes(n)
        return nodes
            
    def walk_subTree(self, node):
        nodes  = self._getAllSubNodes(node)
        for n in nodes:
            self.on_visit(n)

