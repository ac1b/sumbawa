#!/usr/bin/env python3
from google.ads.googleads.client import GoogleAdsClient
import os

# Create client with credentials from environment
credentials = {
    "developer_token": os.environ.get('GOOGLE_ADS_DEVELOPER_TOKEN'),
    "refresh_token": os.environ.get('GOOGLE_ADS_REFRESH_TOKEN'),
    "client_id": os.environ.get('GOOGLE_ADS_CLIENT_ID'),
    "client_secret": os.environ.get('GOOGLE_ADS_CLIENT_SECRET'),
    "login_customer_id": os.environ.get('GOOGLE_ADS_LOGIN_CUSTOMER_ID'),
    "use_proto_plus": True,
}

client = GoogleAdsClient.load_from_dict(credentials)
customer_id = os.environ.get('GOOGLE_ADS_CUSTOMER_ID')

# First, create a bidding strategy
bidding_strategy_service = client.get_service("BiddingStrategyService")

bidding_strategy_operation = client.get_type("BiddingStrategyOperation")
bidding_strategy = bidding_strategy_operation.create
bidding_strategy.name = "Test - Manual CPC Strategy"
bidding_strategy.type_ = "MANUAL_CPC"

try:
    mutate_response = bidding_strategy_service.mutate_bidding_strategies(
        customer_id=customer_id,
        operations=[bidding_strategy_operation],
    )
    print(f"Bidding Strategy created: {mutate_response.results[0].resource_name}")
    bidding_strategy_id = mutate_response.results[0].resource_name
    
    # Now create campaign with this bidding strategy
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = "Test - Sumbawa Land Search"
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.campaign_budget = f"customers/{customer_id}/campaignBudgets/15417028513"
    campaign.bidding_strategy = bidding_strategy_id
    
    mutate_response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[campaign_operation],
    )
    print(f"SUCCESS! Campaign created: {mutate_response.results[0].resource_name}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
