import { defineStore } from 'pinia'

export const useFlightSearchStore = defineStore('flightSearch', {
  state: () => ({
    from: '',
    to: '',
    dateGo: '',
    dateReturn: '',
    passengers: 1,
    ticketClass: 'economy',
    ticketType: 'oneway'
  }),
  actions: {
    setFrom(value) {
      this.from = value
    },
    setTo(value) {
      this.to = value
    },
    setDateGo(value) {
      this.dateGo = value
    },
    setDateReturn(value) {
      this.dateReturn = value
    },
    setPassengers(value) {
      this.passengers = value
    },
    setTicketClass(value) {
      this.ticketClass = value
    },
    setTicketType(value) {
      this.ticketType = value
    }
  }
})
