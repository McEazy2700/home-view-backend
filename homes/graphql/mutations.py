import strawberry

from homes.graphql.types import CountryType, HomeType, LGAType, LocationType, NewHomeInput, NewLocationInput, StateType
from homes.models.models import LGA, Country, Home, Location, State


@strawberry.type
class HomeMutations:
    @strawberry.mutation
    def new_country(self, name: str, country_code: str) -> CountryType:
        return Country.objects().new(name=name, country_code=country_code).gql

    @strawberry.mutation
    def new_state(self, name: str, country_id: int) -> StateType:
        return State.objects().new(name=name, country_id=country_id).gql

    @strawberry.mutation
    def new_lga(self, name: str, state_id: int) -> LGAType:
        return LGA.objects().new(name=name, state_id=state_id).gql

    @strawberry.mutation
    def new_location(self, input: NewLocationInput) -> LocationType:
        new_location = Location.objects().new(
                address=input.address,
                latitude=input.latitude,
                longitude=input.longitude,
                lga_id=input.lga_id
            )
        return new_location.gql

    @strawberry.mutation
    def new_home(self, input: NewHomeInput) -> HomeType:
        new_home = Home.objects().new(
                name=input.name,
                description=input.description,
                location_id=input.location_id,
                room_count=input.room_count)
        return new_home.gql
