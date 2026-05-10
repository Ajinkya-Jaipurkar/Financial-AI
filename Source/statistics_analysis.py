"""
Univariate return distribution analysis for SPY.

Loads the cleaned SPY CSV from the project's Data folder, plots the
distribution of daily returns with an overlaid normal curve, computes
skewness and kurtosis, runs the Jarque-Bera test for normality, and
prints/saves results for inspection.

Designed for Day 2 exploratory analysis and learning.
"""

from pathlib import Path
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_spy_csv(data_dir: Path) -> pd.DataFrame:
	path = data_dir / 'SPY_clean.csv'
	if not path.exists():
		logger.error(f"SPY CSV not found at {path}. Run the data pipeline first.")
		raise FileNotFoundError(path)

	df = pd.read_csv(path, parse_dates=['Date'])
	logger.info(f"Loaded {len(df)} rows from {path}")
	return df


def ensure_returns(df: pd.DataFrame) -> pd.Series:
	# Prefer precomputed Daily_Return, otherwise compute from Close
	if 'Daily_Return' in df.columns:
		returns = df['Daily_Return'].copy()
	else:
		returns = df['Close'].pct_change()

	# Drop missing/inf values
	returns = returns.replace([np.inf, -np.inf], np.nan).dropna()
	return returns


def plot_return_distribution(returns: pd.Series, out_path: Path) -> None:
	mu = returns.mean()
	sigma = returns.std(ddof=0)

	x_min, x_max = returns.min(), returns.max()
	x = np.linspace(x_min, x_max, 1000)
	normal_pdf = stats.norm.pdf(x, loc=mu, scale=sigma)

	# Create a 1x2 subplot figure
	fig, axes = plt.subplots(1, 2, figsize=(14, 5))
	
	# Left panel: Histogram with normal overlay
	ax0 = axes[0]
	ax0.hist(returns, bins=50, density=True, alpha=0.6, color='C0', label='Empirical')
	ax0.plot(x, normal_pdf, 'r--', linewidth=2, label='Normal (fit)')
	ax0.set_title('SPY Daily Return Distribution')
	ax0.set_xlabel('Daily Return')
	ax0.set_ylabel('Density')
	ax0.legend()
	ax0.grid(True, alpha=0.3)

	# Right panel: Q-Q plot
	ax1 = axes[1]
	stats.probplot(returns, dist="norm", plot=ax1)
	ax1.set_title('Q-Q Plot (SPY Returns vs Normal)')
	ax1.grid(True, alpha=0.3)

	plt.tight_layout()
	out_file = out_path / 'spy_return_dist.png'
	plt.savefig(out_file, dpi=150, bbox_inches='tight')
	logger.info(f"Saved return distribution plot to {out_file}")
	plt.close()


def compute_statistics(returns: pd.Series) -> dict:
	# Use bias=False for sample skew/kurtosis; operate on numpy array to satisfy type-checkers
	arr = np.asarray(returns)
	sk = stats.skew(arr, bias=False)
	# scipy.stats.kurtosis returns Fisher's definition (excess kurtosis) by default
	kurt = stats.kurtosis(arr, fisher=True, bias=False)

	jb_stat, jb_p = stats.jarque_bera(arr)

	return {
		'mean': returns.mean(),
		'std': returns.std(ddof=0),
		'skewness': sk,
		'kurtosis_excess': kurt,
		'jarque_bera_stat': jb_stat,
		'jarque_bera_pvalue': jb_p,
		'n': len(returns)
	}


def interpret_results(stats_dict: dict) -> str:
	lines = []
	lines.append(f"N = {stats_dict['n']}")
	lines.append(f"Mean = {stats_dict['mean']:.6f}")
	lines.append(f"Std = {stats_dict['std']:.6f}")
	lines.append(f"Skewness = {stats_dict['skewness']:.4f} (negative => left tail, positive => right tail)")
	lines.append(f"Excess Kurtosis = {stats_dict['kurtosis_excess']:.4f} (0 => normal tails, >0 => heavy tails)")
	lines.append(f"Jarque-Bera stat = {stats_dict['jarque_bera_stat']:.3f}")
	lines.append(f"Jarque-Bera p-value = {stats_dict['jarque_bera_pvalue']:.4f}")

	# Simple interpretation
	alpha = 0.05
	if stats_dict['jarque_bera_pvalue'] < alpha:
		lines.append(f"Interpretation: Reject the null hypothesis of normality at alpha={alpha} (data is NOT normal).")
	else:
		lines.append(f"Interpretation: Cannot reject the null hypothesis of normality at alpha={alpha} (data may be normal).")

	# Add guidance about skew/kurtosis
	if abs(stats_dict['skewness']) > 0.5:
		lines.append("Note: Skewness magnitude > 0.5 indicates appreciable asymmetry in returns.")
	if stats_dict['kurtosis_excess'] > 1:
		lines.append("Note: Excess kurtosis > 1 indicates fat tails (higher probability of extreme returns).")

	return "\n".join(lines)


def main():
	project_root = Path(__file__).parent.parent
	data_dir = project_root / 'Data'
	out_dir = project_root / 'Output'
	out_dir.mkdir(parents=True, exist_ok=True)

	df = load_spy_csv(data_dir)
	returns = ensure_returns(df)

	if returns.empty:
		logger.error("No returns available for analysis.")
		return

	stats_dict = compute_statistics(returns)

	# Print statistics and interpretation
	interpretation = interpret_results(stats_dict)
	print("\n=== SPY Return Distribution Summary ===\n")
	print(interpretation)
	print("\nSaved plot to Data/spy_return_dist.png")

	# Plot and save
	plot_return_distribution(returns, out_dir)


if __name__ == '__main__':
	main()



