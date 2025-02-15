import streamlit as st
import numpy as np

def check_winner(board):
    for row in board:
        if all(cell == "X" for cell in row):
            return "X"
        elif all(cell == "O" for cell in row):
            return "O"
    
    for col in range(3):
        if all(board[row][col] == "X" for row in range(3)):
            return "X"
        elif all(board[row][col] == "O" for row in range(3)):
            return "O"
    
    if all(board[i][i] == "X" for i in range(3)) or all(board[i][2-i] == "X" for i in range(3)):
        return "X"
    elif all(board[i][i] == "O" for i in range(3)) or all(board[i][2-i] == "O" for i in range(3)):
        return "O"
    
    if all(cell != "" for row in board for cell in row):
        return "Draw"
    
    return None

def main():
    st.title("Tic-Tac-Toe")
    
    if "board" not in st.session_state:
        st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
        st.session_state.current_player = "X"
        st.session_state.winner = None
    
    def reset_board():
        st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
        st.session_state.current_player = "X"
        st.session_state.winner = None
    
    def make_move(row, col):
        if st.session_state.board[row][col] == "" and not st.session_state.winner:
            st.session_state.board[row][col] = st.session_state.current_player
            st.session_state.winner = check_winner(st.session_state.board)
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
    
    button_style = """
        <style>
        div.stButton > button {
            width: 100px;
            height: 100px;
            font-size: 24px;
            font-weight: bold;
        }
        .red { background-color: red !important; color: white !important; }
        .blue { background-color: blue !important; color: white !important; }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            value = st.session_state.board[row][col]
            btn_class = "red" if value == "X" else "blue" if value == "O" else ""
            cols[col].markdown(f'<button class="{btn_class}" onclick="{make_move(row, col)}">{value or " "}</button>', unsafe_allow_html=True)
    
    if st.session_state.winner:
        if st.session_state.winner == "Draw":
            st.subheader("It's a draw!")
        else:
            st.subheader(f"{st.session_state.winner} wins!")
        st.button("Restart Game", on_click=reset_board)

if __name__ == "__main__":
    main()
