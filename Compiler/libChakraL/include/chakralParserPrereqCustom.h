#pragma once
    
#include <list>
#include <string>
#include <map>
#include <set>
#include <memory>
#include "chakralParserPrereqShared.h"

namespace ChakraL {
    
    class SemanticNodeVariable {
    public:
        SemanticNodePtr ptr;
        bool trySet(SemanticNodePtr newPtr);
        
        inline SemanticNodeVariable(): ptr(nullptr) {}
        SemanticNodeVariable(const SemanticNodeVariable&) = default;
        SemanticNodeVariable(SemanticNodeVariable&&) = default;
        SemanticNodeVariable(nullptr_t) {ptr = nullptr;}
        SemanticNodeVariable(SemanticNodePtr newPtr) {ptr = newPtr;}
        SemanticNodeVariable& operator = (const SemanticNodeVariable&) = default;
        SemanticNodeVariable& operator = (SemanticNodeVariable&&) = default;
        inline SemanticNodeVariable& operator = (nullptr_t) {ptr = nullptr; return *this;}
        inline SemanticNodeVariable& operator = (SemanticNodePtr newPtr) {ptr = newPtr; return *this;}
        inline SemanticNode& operator *() {return *ptr;}
        inline operator SemanticNodePtr&() {return ptr;}
        inline operator bool() {return (ptr != nullptr);}
        inline SemanticNodePtr operator ->() {return ptr;}
    };
    
    class SemanticNode {
    public:
        virtual ~SemanticNode();
        virtual void process() = 0;
        virtual std::string_view name() const = 0;
        void pullFrom(SemanticNode& other);
        
        std::map<std::string, std::list<SemanticNodeVariable>> nodeLists;
        std::map<std::string, std::list<Token>> tokenLists;
        SemanticNodeVariable continuationNode = nullptr;
        SemanticNodeVariable replacementNode = nullptr;
        bool isSuccessful = true;
        size_t errorSubnodesNum = 0;
        
        std::list<ParserError> errors;
    };

	// State utils
	struct StateSet;
	struct State;
	using StatePtr = std::shared_ptr<State>;
	using NextFuncT = bool (*)(StatePtr curState, StateSet& nextStates, const Token& token, bool isSuccessful);// returns whether the token matches. Node must be used instead of state.node for new states
	
	struct State {
		NextFuncT nextFunc;
		std::set<StatePtr> parentStates;
		// This points to the current node, where we store the variables
		SemanticNodePtr node = nullptr;
		std::list<SemanticNodeVariable*> outputVars;// save to vars on confirm
		size_t childStateCtr = 0;
		
		inline State(NextFuncT nextFunc): nextFunc(nextFunc) {}
		State() = default;
		State(const State&) = default;
		State(State&&) = default;
		State& operator=(const State&) = default;
		State& operator=(State&&) = default;
		
	};
	
	struct StateComparatorLess {
		using is_transparent = std::true_type;
		
		inline bool operator()(const StatePtr& left, const StatePtr& right) const {
			return (left->nextFunc < right->nextFunc);
		}
		inline bool operator()(const NextFuncT& left, const StatePtr& right) const {
			return (left < right->nextFunc);
		}
		inline bool operator()(const StatePtr& left, const NextFuncT& right) const {
			return (left->nextFunc < right);
		}
	};
	
	class StateSet {
	public:
		std::set<StatePtr, StateComparatorLess> stdSet;
		std::set<StatePtr, StateComparatorLess> stdSetHidden;
		
		inline StatePtr operator[](NextFuncT nextFunc) {
			auto it = stdSet.find(nextFunc);
			if (it == stdSet.end()) {
				it = stdSetHidden.find(nextFunc);
				if (it == stdSetHidden.end()) {
					it = stdSet.insert(std::make_shared<State>(nextFunc)).first;
				} else {
					StatePtr statePtr = *it;
					stdSetHidden.erase(it);
					it = stdSet.insert(statePtr).first;
				}
			}
			return *it;
		}
		inline StatePtr getHidden(NextFuncT nextFunc) {
			auto it = stdSet.find(nextFunc);
			if (it == stdSet.end()) {
				it = stdSetHidden.find(nextFunc);
				if (it == stdSetHidden.end()) {
					it = stdSetHidden.insert(std::make_shared<State>(nextFunc)).first;
				}
			}
			return *it;
		}
		
		inline size_t size() const {return stdSet.size();}
		inline std::set<StatePtr, StateComparatorLess>::iterator begin() {return stdSet.begin();}
		inline std::set<StatePtr, StateComparatorLess>::iterator end() {return stdSet.end();}
		
	};
	
    SemanticNodePtr getOrganized(SemanticNodePtr node, bool checkReplacement = true);
	void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors);

}