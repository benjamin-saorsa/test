import random
from typing import List, Dict, Tuple, Optional

class ChessPredictor:
    def __init__(self):
        self.piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100
        }
        
        self.position_bonus = {
            'P': [[ 0,  0,  0,  0,  0,  0,  0,  0],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [10, 10, 20, 30, 30, 20, 10, 10],
                  [ 5,  5, 10, 25, 25, 10,  5,  5],
                  [ 0,  0,  0, 20, 20,  0,  0,  0],
                  [ 5, -5,-10,  0,  0,-10, -5,  5],
                  [ 5, 10, 10,-20,-20, 10, 10,  5],
                  [ 0,  0,  0,  0,  0,  0,  0,  0]],
            
            'N': [[-50,-40,-30,-30,-30,-30,-40,-50],
                  [-40,-20,  0,  0,  0,  0,-20,-40],
                  [-30,  0, 10, 15, 15, 10,  0,-30],
                  [-30,  5, 15, 20, 20, 15,  5,-30],
                  [-30,  0, 15, 20, 20, 15,  0,-30],
                  [-30,  5, 10, 15, 15, 10,  5,-30],
                  [-40,-20,  0,  5,  5,  0,-20,-40],
                  [-50,-40,-30,-30,-30,-30,-40,-50]]
        }

    def parse_fen(self, fen: str) -> Tuple[List[List[str]], str]:
        parts = fen.split()
        board_fen = parts[0]
        turn = parts[1]
        
        board = []
        for rank in board_fen.split('/'):
            row = []
            for char in rank:
                if char.isdigit():
                    row.extend(['.'] * int(char))
                else:
                    row.append(char)
            board.append(row)
        
        return board, turn

    def get_piece_moves(self, board: List[List[str]], row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        moves = []
        piece_type = piece.lower()
        is_white = piece.isupper()
        
        if piece_type == 'p':
            direction = -1 if is_white else 1
            start_row = 6 if is_white else 1
            
            if 0 <= row + direction < 8 and board[row + direction][col] == '.':
                moves.append((row + direction, col))
                
                if row == start_row and board[row + 2 * direction][col] == '.':
                    moves.append((row + 2 * direction, col))
            
            for dc in [-1, 1]:
                new_row, new_col = row + direction, col + dc
                if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                    board[new_row][new_col] != '.' and
                    board[new_row][new_col].isupper() != is_white):
                    moves.append((new_row, new_col))
        
        elif piece_type == 'r':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            moves.extend(self._get_sliding_moves(board, row, col, directions, is_white))
        
        elif piece_type == 'b':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves.extend(self._get_sliding_moves(board, row, col, directions, is_white))
        
        elif piece_type == 'q':
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            moves.extend(self._get_sliding_moves(board, row, col, directions, is_white))
        
        elif piece_type == 'n':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < 8 and 0 <= new_col < 8 and
                    (board[new_row][new_col] == '.' or board[new_row][new_col].isupper() != is_white)):
                    moves.append((new_row, new_col))
        
        elif piece_type == 'k':
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < 8 and 0 <= new_col < 8 and
                    (board[new_row][new_col] == '.' or board[new_row][new_col].isupper() != is_white)):
                    moves.append((new_row, new_col))
        
        return moves

    def _get_sliding_moves(self, board: List[List[str]], row: int, col: int, 
                          directions: List[Tuple[int, int]], is_white: bool) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                if board[new_row][new_col] == '.':
                    moves.append((new_row, new_col))
                else:
                    if board[new_row][new_col].isupper() != is_white:
                        moves.append((new_row, new_col))
                    break
        return moves

    def get_all_moves(self, board: List[List[str]], is_white_turn: bool) -> List[Tuple[int, int, int, int]]:
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.' and piece.isupper() == is_white_turn:
                    piece_moves = self.get_piece_moves(board, row, col, piece)
                    for new_row, new_col in piece_moves:
                        moves.append((row, col, new_row, new_col))
        return moves

    def evaluate_board(self, board: List[List[str]]) -> float:
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    piece_value = self.piece_values[piece]
                    position_value = 0
                    
                    if piece.upper() in self.position_bonus:
                        if piece.isupper():
                            position_value = self.position_bonus[piece.upper()][row][col]
                        else:
                            position_value = -self.position_bonus[piece.upper()][7-row][col]
                    
                    score += piece_value + position_value / 100
        
        return score

    def make_move(self, board: List[List[str]], move: Tuple[int, int, int, int]) -> List[List[str]]:
        new_board = [row[:] for row in board]
        from_row, from_col, to_row, to_col = move
        new_board[to_row][to_col] = new_board[from_row][from_col]
        new_board[from_row][from_col] = '.'
        return new_board

    def minimax(self, board: List[List[str]], depth: int, is_maximizing: bool, 
                alpha: float = float('-inf'), beta: float = float('inf')) -> float:
        if depth == 0:
            return self.evaluate_board(board)
        
        moves = self.get_all_moves(board, is_maximizing)
        if not moves:
            return self.evaluate_board(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score = self.minimax(new_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score = self.minimax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def predict_best_move(self, fen: str, depth: int = 3) -> Optional[str]:
        board, turn = self.parse_fen(fen)
        is_white_turn = turn == 'w'
        
        moves = self.get_all_moves(board, is_white_turn)
        if not moves:
            return None
        
        best_move = None
        best_score = float('-inf') if is_white_turn else float('inf')
        
        for move in moves:
            new_board = self.make_move(board, move)
            score = self.minimax(new_board, depth - 1, not is_white_turn)
            
            if is_white_turn and score > best_score:
                best_score = score
                best_move = move
            elif not is_white_turn and score < best_score:
                best_score = score
                best_move = move
        
        if best_move:
            from_row, from_col, to_row, to_col = best_move
            from_square = chr(ord('a') + from_col) + str(8 - from_row)
            to_square = chr(ord('a') + to_col) + str(8 - to_row)
            return f"{from_square}{to_square}"
        
        return None

def main():
    predictor = ChessPredictor()
    
    print("Chess Move Predictor")
    print("Enter FEN notation or 'quit' to exit")
    print("Example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    while True:
        fen = input("\nEnter FEN: ").strip()
        
        if fen.lower() == 'quit':
            break
        
        if not fen:
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            print("Using starting position")
        
        try:
            best_move = predictor.predict_best_move(fen)
            if best_move:
                print(f"Predicted best move: {best_move}")
            else:
                print("No legal moves found")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()