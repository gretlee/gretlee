"""
Simulation Engine Service
Handles what-if scenario simulations for sustainability planning
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ml_models.energy_demand_model import predict_city_energy_demand
from backend.services.data_loader import data_loader


class SimulationEngine:
    """
    Engine for running sustainability scenario simulations
    """
    
    def __init__(self):
        """
        Initialize simulation engine
        """
        pass
    
    def run_scenario(self, city, scenario_params):
        """
        Run a what-if scenario simulation
        
        Args:
            city: City name
            scenario_params: Dictionary with scenario parameters
                - solar_percentage: Solar energy adoption (0-100)
                - green_spaces_increase: Increase in green spaces percentage
                - electric_transport_percentage: Electric vehicle adoption
                - tree_planting: Number of trees to plant
                - policy_changes: List of policy names
        
        Returns:
            Dictionary with simulation results
        """
        try:
            # Get baseline city data
            city_metadata = data_loader.get_city_metadata(city)
            
            # Initialize results
            results = {
                'city': city,
                'scenario': scenario_params,
                'impacts': {}
            }
            
            # 1. Energy Impact
            energy_scenario = {}
            if 'solar_percentage' in scenario_params:
                energy_scenario['solar_percentage'] = scenario_params['solar_percentage']
            if 'green_spaces_increase' in scenario_params:
                energy_scenario['green_spaces_increase'] = scenario_params['green_spaces_increase']
            if 'electric_transport_percentage' in scenario_params:
                energy_scenario['electric_transport_percentage'] = scenario_params['electric_transport_percentage']
            
            if energy_scenario:
                energy_result = predict_city_energy_demand(city, scenario=energy_scenario)
                results['impacts']['energy'] = energy_result
            
            # 2. Air Quality Impact
            aqi_impact = self._calculate_aqi_impact(city, scenario_params)
            results['impacts']['air_quality'] = aqi_impact
            
            # 3. Carbon Emissions Impact
            carbon_impact = self._calculate_carbon_impact(city, scenario_params, city_metadata)
            results['impacts']['carbon_emissions'] = carbon_impact
            
            # 4. Green Space Impact
            green_impact = self._calculate_green_space_impact(city, scenario_params, city_metadata)
            results['impacts']['green_spaces'] = green_impact
            
            # 5. SDG Alignment Score
            sdg_score = self._calculate_sdg_alignment(scenario_params)
            results['sdg_alignment'] = sdg_score
            
            # 6. Overall Sustainability Score
            sustainability_score = self._calculate_sustainability_score(results)
            results['sustainability_score'] = sustainability_score
            
            return {
                'status': 'success',
                'data': results
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'city': city
            }
    
    def _calculate_aqi_impact(self, city, scenario_params):
        """
        Calculate impact on air quality
        """
        # Baseline AQI (mock - simplified)
        baseline_aqi = 150  # Unhealthy range
        
        # Calculate improvements
        improvement = 0
        
        # Solar energy reduces fossil fuel burning
        if 'solar_percentage' in scenario_params:
            improvement += scenario_params['solar_percentage'] * 0.2
        
        # Green spaces filter air
        if 'green_spaces_increase' in scenario_params:
            improvement += scenario_params['green_spaces_increase'] * 0.15
        
        # Electric transport reduces emissions
        if 'electric_transport_percentage' in scenario_params:
            improvement += scenario_params['electric_transport_percentage'] * 0.25
        
        # Tree planting
        if 'tree_planting' in scenario_params:
            trees = scenario_params['tree_planting']
            improvement += min(20, trees / 10000)  # Max 20 point improvement
        
        new_aqi = max(50, baseline_aqi - improvement)
        
        return {
            'baseline_aqi': baseline_aqi,
            'projected_aqi': round(new_aqi, 1),
            'improvement': round(baseline_aqi - new_aqi, 1),
            'improvement_percentage': round((baseline_aqi - new_aqi) / baseline_aqi * 100, 1)
        }
    
    def _calculate_carbon_impact(self, city, scenario_params, city_metadata):
        """
        Calculate impact on carbon emissions
        """
        population = city_metadata['population']
        
        # Baseline per capita emissions (tons CO2/year)
        baseline_per_capita = 2.5
        baseline_total = population * baseline_per_capita
        
        # Calculate reductions
        reduction_factor = 0
        
        if 'solar_percentage' in scenario_params:
            reduction_factor += scenario_params['solar_percentage'] / 100 * 0.3
        
        if 'electric_transport_percentage' in scenario_params:
            reduction_factor += scenario_params['electric_transport_percentage'] / 100 * 0.2
        
        if 'tree_planting' in scenario_params:
            # Trees absorb CO2 (approx 20kg per tree per year)
            trees = scenario_params['tree_planting']
            tree_absorption = (trees * 20) / 1000  # Convert to tons
        else:
            tree_absorption = 0
        
        new_total = baseline_total * (1 - reduction_factor) - tree_absorption
        
        return {
            'baseline_tons_co2': round(baseline_total, 0),
            'projected_tons_co2': round(max(0, new_total), 0),
            'reduction_tons': round(baseline_total - new_total, 0),
            'reduction_percentage': round((baseline_total - new_total) / baseline_total * 100, 1),
            'tree_contribution_tons': round(tree_absorption, 0)
        }
    
    def _calculate_green_space_impact(self, city, scenario_params, city_metadata):
        """
        Calculate impact on green spaces
        """
        area_km2 = city_metadata['area_km2']
        
        # Baseline green space (assume 10% of city area)
        baseline_percentage = 10
        baseline_area = area_km2 * baseline_percentage / 100
        
        # Calculate new green space
        if 'green_spaces_increase' in scenario_params:
            increase = scenario_params['green_spaces_increase']
            new_percentage = baseline_percentage + increase
        else:
            new_percentage = baseline_percentage
        
        new_area = area_km2 * new_percentage / 100
        
        return {
            'baseline_percentage': baseline_percentage,
            'projected_percentage': round(new_percentage, 1),
            'baseline_area_km2': round(baseline_area, 2),
            'projected_area_km2': round(new_area, 2),
            'increase_km2': round(new_area - baseline_area, 2)
        }
    
    def _calculate_sdg_alignment(self, scenario_params):
        """
        Calculate alignment with UN SDGs
        """
        sdg_scores = {}
        
        # SDG 7: Affordable and Clean Energy
        if 'solar_percentage' in scenario_params:
            sdg_scores['SDG_7'] = min(100, scenario_params['solar_percentage'] * 2)
        else:
            sdg_scores['SDG_7'] = 30
        
        # SDG 11: Sustainable Cities
        score_11 = 40
        if 'green_spaces_increase' in scenario_params:
            score_11 += min(30, scenario_params['green_spaces_increase'])
        if 'electric_transport_percentage' in scenario_params:
            score_11 += min(30, scenario_params['electric_transport_percentage'] * 0.5)
        sdg_scores['SDG_11'] = min(100, score_11)
        
        # SDG 13: Climate Action
        score_13 = 35
        if 'solar_percentage' in scenario_params:
            score_13 += min(35, scenario_params['solar_percentage'] * 0.5)
        if 'tree_planting' in scenario_params:
            score_13 += min(30, scenario_params['tree_planting'] / 5000)
        sdg_scores['SDG_13'] = min(100, score_13)
        
        # SDG 3: Good Health (air quality)
        score_3 = 40
        if 'green_spaces_increase' in scenario_params:
            score_3 += min(30, scenario_params['green_spaces_increase'])
        if 'electric_transport_percentage' in scenario_params:
            score_3 += min(30, scenario_params['electric_transport_percentage'] * 0.4)
        sdg_scores['SDG_3'] = min(100, score_3)
        
        # Overall SDG score
        overall_score = sum(sdg_scores.values()) / len(sdg_scores)
        
        return {
            'individual_scores': sdg_scores,
            'overall_score': round(overall_score, 1),
            'rating': self._get_rating(overall_score)
        }
    
    def _calculate_sustainability_score(self, results):
        """
        Calculate overall sustainability score (0-100)
        """
        score = 0
        
        # Energy efficiency (25%)
        if 'energy' in results['impacts']:
            energy = results['impacts']['energy']
            if 'change_percentage' in energy:
                # Negative change is good (reduced demand)
                score += max(0, min(25, -energy['change_percentage']))
        
        # Air quality improvement (25%)
        if 'air_quality' in results['impacts']:
            aqi = results['impacts']['air_quality']
            score += min(25, aqi.get('improvement_percentage', 0) * 2.5)
        
        # Carbon reduction (25%)
        if 'carbon_emissions' in results['impacts']:
            carbon = results['impacts']['carbon_emissions']
            score += min(25, carbon.get('reduction_percentage', 0) * 2.5)
        
        # SDG alignment (25%)
        if 'sdg_alignment' in results:
            score += results['sdg_alignment']['overall_score'] * 0.25
        
        return {
            'score': round(score, 1),
            'rating': self._get_rating(score),
            'description': self._get_score_description(score)
        }
    
    def _get_rating(self, score):
        """Get rating based on score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Moderate'
        else:
            return 'Needs Improvement'
    
    def _get_score_description(self, score):
        """Get description for sustainability score"""
        if score >= 80:
            return 'Outstanding sustainability impact with significant improvements across all metrics'
        elif score >= 60:
            return 'Strong sustainability improvements with positive environmental impact'
        elif score >= 40:
            return 'Moderate improvements with room for enhanced sustainability measures'
        else:
            return 'Limited sustainability impact, consider more aggressive interventions'


# Singleton instance
simulation_engine = SimulationEngine()
