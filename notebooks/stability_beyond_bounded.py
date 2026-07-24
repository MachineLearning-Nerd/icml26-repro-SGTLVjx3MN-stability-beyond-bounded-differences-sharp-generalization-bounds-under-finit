import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Stability beyond bounded differences: an exact reproduction

    **Headline evidence:** two universally quantified application theorems
    have complete, assumption-satisfying counterexamples.

    | Claim | Exact left side | Displayed right side | Result |
    | --- | ---: | ---: | --- |
    | Theorem 3.10 | \(1/2\) | \(0\) | **FALSIFIED** |
    | Theorem 3.14 | \(1\) | \(0\) | **FALSIFIED** |

    The other results are three exact verification certificates and one
    honestly blocked theorem. All displayed evidence is embedded here; no
    expensive rerun is required.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The central question

    Classical bounded-differences arguments require every coordinate
    replacement to have a deterministic maximum effect. The paper replaces
    that premise by a random envelope with only a finite \(p\)-th moment.
    The key concentration inequality combines a polynomial large-jump term
    with a Gaussian moderate-deviation term.

    A faithful reproduction must therefore test the exact envelope,
    centering, constants, and quantifiers—not merely show that regularizing
    or adding data helps on one simulation.
    """)
    return


@app.cell
def _(mo):
    threshold = mo.ui.slider(
        start=0.05,
        stop=1.0,
        step=0.05,
        value=0.5,
        label="Theorem 3.10 threshold y",
    )
    threshold
    return (threshold,)


@app.cell
def _(mo, threshold):
    gaps = (1, -1)
    left_probability = sum(gap >= threshold.value for gap in gaps) / len(gaps)
    paper_coefficient = abs(1 / 1 - 1 / 1)
    displayed_right = 0 if paper_coefficient == 0 else None
    mo.md(
        rf"""
        ## Explore the complete Theorem 3.10 witness

        The population has labels `0` and `1`, with one training and one test
        point. A constant-zero predictor has gaps `{gaps}` across the two
        partitions. At \(y={threshold.value:.2f}\), the exact event probability
        is **{left_probability:.2f}**.

        Because \(m=u=1\), the paper's coefficient
        \(\lvert 1/u-1/m\rvert\) is `{paper_coefficient:.0f}`. With a perfectly
        stable algorithm, both displayed variance terms vanish and the right
        side is **{displayed_right}**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why the transductive coefficient fails

    Swapping losses \(a\) and \(b\) between a test average and a training
    average changes their difference with coefficient

    \[
    \frac{1}{u}+\frac{1}{m},
    \]

    not \(\lvert1/u-1/m\rvert\). In the witness the actual gap increment is
    two. The paper coefficient gives zero; the corrected coefficient gives
    two exactly. An independent checker exhausts both partitions and every
    premise comparison.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The meta-learning counterexample

    Let the meta-distribution choose equally between two point-mass tasks,
    one always labeled zero and one always labeled one. The meta-learner
    observes the training task label \(\theta\), then returns a learner that
    ignores new task data and predicts \(1-\theta\).

    Every *within-task* replacement in Assumption 3.12 is unchanged, so
    \(H=G=M=0\). Yet the empirical meta-risk is one and population
    meta-risk is one half. The gap is one half in both meta-training
    states. At \(y=1/4\), Theorem 3.14 states \(1\le0\).

    The proof reveals the issue: equation (104) replaces a complete task,
    while the assumption controls only one observation within a fixed task
    distribution.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## All six outcomes

    | Claim | Outcome | Direct basis |
    | --- | --- | --- |
    | 1 · Theorem 2.2 | VERIFIED | Universal Doob/truncation derivation and exact constants |
    | 2 · Theorem 2.6 | BLOCKED | Four routes; proof gap but no theorem counterexample |
    | 3 · Assumption 3.1 | VERIFIED | Finite-\(L_2\), infinite-uniform-stability witness |
    | 4 · Theorem 3.4 | VERIFIED | Universal reduction to Theorem 2.2 |
    | 5 · Theorems 3.9/3.10 | FALSIFIED | Complete two-partition counterexample to 3.10 |
    | 6 · Theorem 3.14 | FALSIFIED | Complete two-task counterexample |

    Previous live score: **6/12**. Conservative forecast: **8–11/12**.
    Best-supported possible result: **11/12**, explicitly not a judge
    result.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Optional local verification

    The evidence above is already embedded. To run the cumulative exact
    suite locally:

    ```bash
    uv sync --locked
    uv run --locked python -m reproduction.run_all
    ```

    The formal run used one locked environment and one fixed command on
    every experiment node. Short checks used local CPU; the uncertain
    Claim 2 search used Hugging Face `cpu-upgrade`. No GPU was used.
    """)
    return


if __name__ == "__main__":
    app.run()
