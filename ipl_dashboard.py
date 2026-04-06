import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def load_dataframe(path, default_df):
    if os.path.exists(path):
        return pd.read_csv(path)
    return default_df


def load_data():
    # Replace these sample DataFrames with your actual analytics outputs or CSV file paths.
    summary_table_df = load_dataframe(
        "summary_table.csv",
        pd.DataFrame(
            {
                "team": ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders", "Royal Challengers Bangalore", "Sunrisers Hyderabad"],
                "total_wins": [115, 104, 95, 88, 79],
                "win_percentage": [58.5, 55.2, 52.8, 49.3, 46.1],
            }
        ),
    )

    toss_impact_percentage = load_dataframe(
        "toss_impact_percentage.csv",
        pd.DataFrame(
            {
                "decision": ["bat", "field"],
                "win_rate": [54.3, 45.7],
                "matches": [320, 280],
            }
        ),
    )

    wins_batting_first_by_score_range = load_dataframe(
        "wins_batting_first_by_score_range.csv",
        pd.DataFrame(
            {
                "score_range": ["< 140", "140-159", "160-179", "180-199", ">= 200"],
                "first_innings_win_pct": [22.0, 45.5, 61.2, 72.8, 85.4],
            }
        ),
    )

    home_away_df = load_dataframe(
        "home_away_df.csv",
        pd.DataFrame(
            {
                "team": ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders", "Royal Challengers Bangalore", "Sunrisers Hyderabad"],
                "home_win_pct": [62.4, 59.8, 54.0, 48.2, 50.6],
                "away_win_pct": [51.9, 49.7, 46.3, 43.1, 41.8],
                "neutral_win_pct": [55.0, 52.1, 50.6, 47.2, 44.0],
            }
        ),
    )

    top_players_of_match = load_dataframe(
        "top_players_of_match.csv",
        pd.DataFrame(
            {
                "player": [
                    "MS Dhoni",
                    "AB de Villiers",
                    "Suresh Raina",
                    "Chris Gayle",
                    "Shane Watson",
                    "Virat Kohli",
                    "David Warner",
                    "Rohit Sharma",
                    "Glenn Maxwell",
                    "Jasprit Bumrah",
                ],
                "awards": [17, 15, 14, 13, 13, 12, 12, 11, 10, 10],
            }
        ),
    )
    
    # If the CSV loaded top_players_of_match into a DataFrame, convert it to a Series for easier use.
    if isinstance(top_players_of_match, pd.DataFrame) and "player" in top_players_of_match.columns:
        top_players_of_match = top_players_of_match.set_index("player")["awards"].sort_values(ascending=False)

    return {
        "summary_table_df": summary_table_df,
        "toss_impact_percentage": toss_impact_percentage,
        "wins_batting_first_by_score_range": wins_batting_first_by_score_range,
        "home_away_df": home_away_df,
        "top_players_of_match": top_players_of_match,
    }


def build_top_teams_chart(summary_table_df):
    fig = px.bar(
        summary_table_df.sort_values("total_wins", ascending=False).head(5),
        x="team",
        y="total_wins",
        text="total_wins",
        title="Top 5 Teams: Total Wins",
        labels={"team": "Team", "total_wins": "Total Wins"},
    )
    fig.add_trace(
        go.Scatter(
            x=summary_table_df["team"],
            y=summary_table_df["win_percentage"],
            mode="lines+markers",
            name="Win Percentage",
            marker=dict(color="#ff7f0e", size=10),
            yaxis="y2",
        )
    )
    fig.update_layout(
        yaxis=dict(title="Total Wins"),
        yaxis2=dict(
            title="Win Percentage (%)",
            overlaying="y",
            side="right",
            rangemode="tozero",
        ),
        legend=dict(x=0.75, y=0.95),
        margin=dict(l=40, r=40, t=70, b=40),
    )
    return fig


def build_toss_impact_chart(toss_impact_percentage):
    return px.bar(
        toss_impact_percentage,
        x="decision",
        y="win_rate",
        text="win_rate",
        title="Toss Decision Impact on Match Outcome",
        labels={"decision": "Toss Decision", "win_rate": "Win Rate (%)"},
        color="decision",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )


def build_first_innings_chart(wins_batting_first_by_score_range):
    return px.bar(
        wins_batting_first_by_score_range,
        x="score_range",
        y="first_innings_win_pct",
        text="first_innings_win_pct",
        title="First Innings Score Influence on Winning Probability",
        labels={
            "score_range": "First Innings Score Range",
            "first_innings_win_pct": "Batting First Win %",
        },
        color="first_innings_win_pct",
        color_continuous_scale="Viridis",
    )


def build_home_away_chart(home_away_df):
    return go.Figure(
        data=[
            go.Bar(name="Home Win %", x=home_away_df["team"], y=home_away_df["home_win_pct"]),
            go.Bar(name="Away Win %", x=home_away_df["team"], y=home_away_df["away_win_pct"]),
            go.Bar(name="Neutral Win %", x=home_away_df["team"], y=home_away_df["neutral_win_pct"]),
        ],
    ).update_layout(
        title="Home vs. Away Performance for Top Teams",
        xaxis_title="Team",
        yaxis_title="Win Percentage (%)",
        barmode="group",
        margin=dict(l=40, r=40, t=70, b=40),
    )


def build_top_players_chart(top_players_of_match):
    if isinstance(top_players_of_match, pd.Series):
        df = top_players_of_match.head(10).reset_index()
        fig = px.bar(
            df,
            x=df.columns[0],
            y=df.columns[1],
            text=df.columns[1],
            title="Top 10 Player of the Match Award Winners",
            labels={df.columns[0]: "Player", df.columns[1]: "Award Count"},
        )
    else:
        fig = px.bar(
            top_players_of_match.head(10),
            x="player",
            y="awards",
            text="awards",
            title="Top 10 Player of the Match Award Winners",
            labels={"player": "Player", "awards": "Award Count"},
        )
    fig.update_layout(xaxis_tickangle=-45, margin=dict(l=40, r=40, t=70, b=100))
    return fig


def create_app():
    data = load_data()

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "IPL Club Analytics Dashboard"

    app.layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("IPL Club Analytics Dashboard", className="text-center my-4"),
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "This dashboard connects IPL performance analytics to club strategy by highlighting team strength, toss decisions, scoring thresholds, home advantage, and match-winning players.",
                        className="lead text-center",
                    ),
                )
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=build_top_teams_chart(data["summary_table_df"])), md=12),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=build_toss_impact_chart(data["toss_impact_percentage"])), md=6),
                    dbc.Col(dcc.Graph(figure=build_first_innings_chart(data["wins_batting_first_by_score_range"])), md=6),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=build_home_away_chart(data["home_away_df"])), md=12),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=build_top_players_chart(data["top_players_of_match"])), md=12),
                ],
                className="mb-4",
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("How the Club Can Use This Dashboard", className="card-title"),
                                html.Ul(
                                    [
                                        html.Li("Focus on top-performing teams and benchmark win percentage targets."),
                                        html.Li("Use toss insights to refine decision-making when winning the toss."),
                                        html.Li("Target first-innings score ranges that maximize batting-first victory chances."),
                                        html.Li("Plan squad rotations around home and away strengths."),
                                        html.Li("Identify high-impact players with frequent Player of the Match awards."),
                                    ]
                                ),
                            ]
                        )
                    ),
                )
            ),
        ],
        fluid=True,
    )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=8050)
