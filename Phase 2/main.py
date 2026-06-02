"""
Phase 2 MVP Demo - Sapien Didactic Episode

Demonstrates:
1. Single learner instance
2. Single teacher model (mock LLM)
3. Basic DAG implementation (knowledge graph)
4. Didactic episode loop
5. SEED node creation
6. WHY chain storage
7. Epistemic closure detection

Run with: python main.py
"""

import sys
import os
from pathlib import Path

from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from graph.dag import DAG
from agents.teacher import DefaultTeacher
from episode.episode_loop import DidacticEpisode, EpisodeConfig


def main():
    """Run the Phase 2 MVP demo."""
    
    print("=" * 70)
    print("SAPIEN PHASE 2 - MINIMAL DIDACTIC EPISODE PROTOTYPE")
    print("=" * 70)
    print()
    print("This MVP demonstrates:")
    print("  ✓ Single learner instance")
    print("  ✓ Single teacher model (mock for this demo)")
    print("  ✓ Basic DAG implementation (SQLite)")
    print("  ✓ Didactic episode loop")
    print("  ✓ SEED node creation")
    print("  ✓ WHY chain storage & validation")
    print("  ✓ Epistemic closure detection")
    print()
    print("=" * 70)
    print()
    
    # Load environment configuration
    script_dir = Path(__file__).resolve().parent
    env_path = script_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        load_dotenv()
        print("Loaded environment variables from the shell environment")

    first_teacher_api = os.getenv("FIRST_TEACHER_API")
    second_teacher_api = os.getenv("SECOND_TEACHER_API")
    judge_api = os.getenv("JUDGE_API")

    # Initialize knowledge graph
    db_path = os.path.join(os.path.dirname(__file__), "knowledge_graph.db")
    
    # Clear database if it exists (for fresh start)
    if os.path.exists(db_path):
        os.remove(db_path)
    
    dag = DAG(db_path)
    print(f"Initialized DAG at: {db_path}")
    
    # Initialize teacher stub for MVP
    teacher = DefaultTeacher(api_key=first_teacher_api)
    print(f"Initialized DefaultTeacher stub (FIRST_TEACHER_API={'SET' if first_teacher_api else 'MISSING'})")
    if second_teacher_api:
        print("SECOND_TEACHER_API is configured")
    if judge_api:
        print("JUDGE_API is configured")
    
    # Configure episode
    config = EpisodeConfig(
        topic="photosynthesis",
        domain="biology",
        max_iterations=5,
        max_questions=3,
        require_deep_chains=False,
    )
    
    # Create and run episode
    episode = DidacticEpisode(config, teacher, dag)
    
    try:
        success = episode.run()
        episode.print_summary()
        
        if success:
            print("\n✓ Episode completed successfully with epistemic closure!")
            return 0
        else:
            print("\nEpisode terminated before closure (expected for MVP with max iterations).")
            return 0
            
    except Exception as e:
        print(f"\n✗ Episode error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
