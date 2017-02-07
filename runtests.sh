echo ""
echo "CORE TESTS"
echo "==================================="
python -m tests/test_core

echo ""
echo "PIECE TESTS"
echo "==================================="
python -m tests/test_pieces

echo ""
echo "VECTOR TESTS"
echo "==================================="
python -m tests/test_vectors

echo ""
echo "GUI & UI TESTS"
echo "==================================="
python -m tests/test_usercontrol

echo ""
echo "CHESSBOARD TESTS"
echo "==================================="
python -m tests/test_chessboard

echo ""
echo "MOVEGEN TESTS"
echo "==================================="
#python -m tests/test_movegenerator
echo "There is nothing here yet..."

echo ""
echo "ENGINE TESTS"
echo "==================================="
#python -m tests/test_engine
echo "There is nothing here yet..."
