"""Included this code to change gino's logging level. This prevents some double
logging that was making my lose my mind with uvicorn's defaults.
"""
import logging

logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)
