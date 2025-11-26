# board ASCII printing

from core.board import Board, CellState

class Renderer:
    """
    Render board state to ASCII art.
    """
    def render(board: Board, reveal_all: bool= False) -> str:
        """
        Render board to string

        Args: Board to render, reveal_all: if true, show all mines.

        Returns: Multi-line ASCII representation
        """

        lines = []
        header = "  " + " ".join(str(i % 10) for i in range(board.width))
        lines.append(header)

        for y in range(board.height):
            row_parts = [f"{y:2}"]
            for x in range(board.width):
                cell_str = Render._render_cell(board, x, y, reveal_all)
            lines.append(" " + " ".join(row_parts))

        
        return "\n".join(lines)

    def _render_cell(board: Board, x: int, y: int, reveal_all: bool) -> str:
        """
        Render single cell.
        """
        state = board.get_state(x, y)

        if state == CellState.FLAGGED:
            return 'F'

        if reveal_all and board.is_mine(x, y):
            return "*"

        if state == CellState.REVEALED:
            if board.is_mine(x, y):
                return "*"
            count = board.get_count(x, y)
            if count == 0:
                return " "
            return str(count)
            
        return "."

    def render_probabilities(board": Board, probabilities: dist) -> str:
        """
        Render probability heatmap for unknown cells.
        """
        lines = []
        header = "  " + " ".join(str(i % 10) for i in range(board.width))
        lines.append(header)

        for i in range(board.height):
            row_parts = [f"{y:2}"]
            for x in range(board.width):
                state = board.get_state(x, y)
                if state == CellState.REVEALED:
                    row_parts.append(" ")
                elif state == CellState.FLAGGED:
                    row_parts.append("F")
                else:
                    prob = probabilities.get((x, y), 0, 0)
                    symbol = Render._prob_to_symbol(prob)
                    row_parts.append(symbol)
            
            lines.append(" " + " ".join(row_parts))
        legend = "n\Legend: . (0%) - (10%) = (20%) + (30-40%) # (50-70%) @ (80-90%) * (100%)"
        lines.append(legend)

        return "\n".join(lines)

    def _prob_to_symbol(prob: float) -> str:
        """
        Convert probability to visual symbol.
        """
        if prob < 0.001:
            return "."
        elif prob < 0.15:
            return "-"
        elif prob < 0.25:
            return "="
        elif prob < 0.45:
            return "+"
        elif prob < 0.75:
            return "#"
        elif prob < 0.95:
            return "@"
        else:
            return "*"
        

    